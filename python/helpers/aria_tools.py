import json
import os
from typing import Any, List, Dict, Tuple
from python.helpers.stable_diffusion import generate_image as _sd_generate

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

try:
    from elevenlabs.client import ElevenLabs
except Exception:  # pragma: no cover - optional dependency
    ElevenLabs = None  # type: ignore

# initialize OpenAI client if library available
client = OpenAI() if OpenAI else None

# tool definitions for Aria
ARIA_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "custom",
        "name": "sd_image",
        "description": "Generate an image from a text prompt using Stable Diffusion.",
    },
    {
        "type": "custom",
        "name": "eleven_tts",
        "description": "Convert text to speech using ElevenLabs.",
    },
    {
        "type": "function",
        "name": "post_to_instagram",
        "description": "Post an image with a caption to Instagram.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string"},
                "caption": {"type": "string"},
            },
            "required": ["image_path", "caption"],
        },
    },
    {
        "type": "function",
        "name": "stripe_checkout",
        "description": "Create a Stripe checkout session and return the payment URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "price_id": {"type": "string"},
                "success_url": {"type": "string"},
                "cancel_url": {"type": "string"},
            },
            "required": ["price_id"],
        },
    },
]

# allowed tool groupings
ALLOWED_IMAGE = [{"type": "custom", "name": "sd_image"}]
ALLOWED_TTS = [{"type": "custom", "name": "eleven_tts"}]
ALLOWED_INSTAGRAM = [{"type": "function", "name": "post_to_instagram"}]
ALLOWED_STRIPE = [{"type": "function", "name": "stripe_checkout"}]

def gpt5(
    prompt: Any,
    tools: List[Dict[str, Any]] | None = None,
    allowed: List[Dict[str, str]] | None = None,
    effort: str = "minimal",
    verbosity: str = "low",
    system_preamble: str | None = None,
    previous_response_id: str | None = None,
):
    """Helper around the Responses API with reasoning/verbosity controls."""
    if not client:
        raise RuntimeError("OpenAI client not available")

    kwargs: Dict[str, Any] = {
        "model": "gpt-5",
        "input": prompt,
        "reasoning": {"effort": effort},
        "text": {"verbosity": verbosity},
    }
    if tools:
        kwargs["tools"] = tools
    if allowed:
        kwargs["tool_choice"] = {
            "type": "allowed_tools",
            "mode": "auto",
            "tools": allowed,
        }
    if system_preamble:
        kwargs["system"] = system_preamble
    if previous_response_id:
        kwargs["previous_response_id"] = previous_response_id
    return client.responses.create(**kwargs)


def _eleven_tts(text: str) -> str:
    """Convert text to speech with ElevenLabs.

    Requires ``ELEVENLABS_API_KEY`` and ``PERSONA_VOICE_ID`` to be set. Raises
    ``RuntimeError`` if the service is not configured or fails."""

    api_key = (os.getenv("ELEVENLABS_API_KEY") or "").strip()
    voice_id = (os.getenv("PERSONA_VOICE_ID") or "").strip()

    if ElevenLabs is None:
        raise RuntimeError("ElevenLabs library not installed")
    if not api_key or not voice_id:
        raise RuntimeError("ELEVENLABS_API_KEY and PERSONA_VOICE_ID must be set")

    client = ElevenLabs(api_key=api_key)
    try:  # pragma: no cover - network interaction
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text,
            output_format="mp3_44100_128",
        )
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", "aria_tts.mp3")
        with open(path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        return path
    except Exception as e:  # pragma: no cover - network interaction
        raise RuntimeError(f"ElevenLabs TTS error: {e}") from e


def _post_to_instagram(image_path: str, caption: str) -> str:
    """Placeholder for posting to Instagram."""
    return f"posted {image_path} with caption {caption}"


def _stripe_checkout(price_id: str, success_url: str | None = None, cancel_url: str | None = None) -> str:
    """Create a Stripe checkout session if Stripe is configured."""
    try:
        from python.helpers.egirl.stripe import create_checkout_session
        return create_checkout_session(price_id, success_url, cancel_url) or ""
    except Exception:
        return ""


def handle_tool_call(msg: Any) -> Tuple[Any, str | None]:
    """Handle tool calls returned by the model.

    Returns a tuple of (followup_response, result_value)
    where result_value may be a path or message from the tool.
    """
    if not client:
        raise RuntimeError("OpenAI client not available")

    if getattr(msg, "type", None) != "tool_call":
        return msg, None

    name = getattr(msg, "name", "")
    result: str | None = None
    error: str | None = None
    if name == "sd_image":
        raw_args = getattr(msg, "arguments", "")
        prompt: str | None = None
        output_dir: str | None = None
        negative_prompt: str | None = None
        seed: int | None = None
        steps: int | None = None
        guidance_scale: float | None = None
        width: int | None = None
        height: int | None = None

        parsed: Dict[str, Any] | None = None

        if isinstance(raw_args, str):
            stripped = raw_args.strip()
            if stripped.startswith("{"):
                try:
                    parsed = json.loads(stripped)
                except json.JSONDecodeError:
                    prompt = stripped
            elif stripped:
                prompt = stripped
        elif isinstance(raw_args, dict):
            parsed = raw_args

        if parsed:
            prompt_val = parsed.get("prompt")
            if isinstance(prompt_val, str):
                prompt = prompt_val
            elif prompt_val is not None:
                prompt = str(prompt_val)

            negative = parsed.get("negative_prompt")
            if isinstance(negative, str):
                negative_prompt = negative

            output_dir_val = parsed.get("output_dir") or parsed.get("output_path")
            if isinstance(output_dir_val, str) and output_dir_val.strip():
                output_dir = output_dir_val.strip()

            def _maybe_int(value: Any) -> int | None:
                if value in (None, ""):
                    return None
                try:
                    return int(value)
                except (TypeError, ValueError):
                    return None

            def _maybe_float(value: Any) -> float | None:
                if value in (None, ""):
                    return None
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return None

            seed = _maybe_int(parsed.get("seed"))
            steps = _maybe_int(parsed.get("steps") or parsed.get("num_inference_steps"))
            width = _maybe_int(parsed.get("width"))
            height = _maybe_int(parsed.get("height"))
            guidance_scale = _maybe_float(parsed.get("guidance_scale") or parsed.get("cfg") or parsed.get("cfg_scale"))

        if not prompt:
            error = "Stable Diffusion tool requires a prompt string"
        else:
            sd_kwargs: Dict[str, Any] = {}
            if output_dir:
                sd_kwargs["output_dir"] = output_dir
            if negative_prompt:
                sd_kwargs["negative_prompt"] = negative_prompt
            if seed is not None:
                sd_kwargs["seed"] = seed
            if steps is not None:
                sd_kwargs["steps"] = steps
            if guidance_scale is not None:
                sd_kwargs["guidance_scale"] = guidance_scale
            if width is not None:
                sd_kwargs["width"] = width
            if height is not None:
                sd_kwargs["height"] = height

            try:
                result = _sd_generate(prompt, **sd_kwargs)
            except Exception as exc:  # pragma: no cover - depends on external services
                error = str(exc)
                result = None
    elif name == "eleven_tts":
        text = getattr(msg, "arguments", "")
        try:
            result = _eleven_tts(text)
        except Exception as e:  # pragma: no cover - network interaction
            error = str(e)
            result = None
    elif name == "post_to_instagram":
        args = getattr(msg, "arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        image_path = args.get("image_path", "")
        caption = args.get("caption", "")
        result = _post_to_instagram(image_path, caption)
    elif name == "stripe_checkout":
        args = getattr(msg, "arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        price_id = args.get("price_id", "")
        success_url = args.get("success_url")
        cancel_url = args.get("cancel_url")
        result = _stripe_checkout(price_id, success_url, cancel_url)
    else:
        return msg, None

    content = {"result": result}
    if error:
        content = {"error": error}

    followup = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "tool",
                "content": json.dumps(content),
                "tool_call_id": getattr(msg, "id", ""),
            }
        ],
        previous_response_id=getattr(msg, "response_id", None),
    )
    return followup, result
