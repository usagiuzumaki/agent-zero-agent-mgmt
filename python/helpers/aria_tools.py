import json
import os
from typing import Any, List, Dict, Tuple
from python.helpers.stable_diffusion import generate_image as _sd_generate
from python.helpers.tunnel_manager import TunnelManager
from python.helpers.egirl import instagram

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
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "seed": {"type": "integer"},
                "steps": {"type": "integer", "minimum": 1},
                "guidance_scale": {"type": "number", "minimum": 0},
                "output_dir": {"type": "string"},
            },
            "required": ["prompt"],
        },
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


def _parse_tool_arguments(raw: Any) -> Dict[str, Any]:
    """Normalize tool arguments into a dictionary."""

    if isinstance(raw, dict):
        return raw

    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return {}
        try:
            loaded = json.loads(text)
        except Exception:
            return {"prompt": text}
        if isinstance(loaded, dict):
            return loaded
        # If it's a list or scalar, return under a generic key
        return {"value": loaded}

    # Unsupported types -> empty dict
    return {}


def _coerce_int(value: Any) -> int | None:
    """Best-effort conversion of ``value`` to ``int``."""

    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return int(float(value))
        except ValueError:
            return None
    return None


def _coerce_float(value: Any) -> float | None:
    """Best-effort conversion of ``value`` to ``float``."""

    if value is None:
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _extract_sd_request(arguments: Any) -> tuple[str | None, Dict[str, Any]]:
    """Extract prompt and keyword arguments for Stable Diffusion."""

    parsed = _parse_tool_arguments(arguments)

    prompt: str | None = None
    if isinstance(parsed, dict):
        prompt = parsed.get("prompt")
        if not prompt:
            if isinstance(parsed.get("input"), dict):
                input_dict = parsed["input"]
                prompt = input_dict.get("prompt") or input_dict.get("text")
            elif isinstance(parsed.get("input"), str):
                prompt = parsed.get("input")
        if not prompt and isinstance(parsed.get("text"), str):
            prompt = parsed.get("text")
    else:
        parsed = {}

    if prompt is None and isinstance(arguments, str):
        stripped = arguments.strip()
        prompt = stripped or None
        parsed = {}

    kwargs: Dict[str, Any] = {}
    if isinstance(parsed, dict):
        if parsed.get("output_dir") is not None:
            kwargs["output_dir"] = parsed["output_dir"]
        if parsed.get("seed") is not None:
            seed = _coerce_int(parsed.get("seed"))
            if seed is not None:
                kwargs["seed"] = seed
        step_value = parsed.get("steps", parsed.get("num_inference_steps"))
        if step_value is not None:
            steps = _coerce_int(step_value)
            if steps and steps > 0:
                kwargs["steps"] = steps
        guidance_value = parsed.get("guidance_scale", parsed.get("cfg"))
        if guidance_value is not None:
            guidance = _coerce_float(guidance_value)
            if guidance is not None and guidance >= 0:
                kwargs["guidance_scale"] = guidance

    return prompt, kwargs

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
    """Post to Instagram using the public tunnel URL."""
    # Get public tunnel URL
    tunnel_url = TunnelManager.get_instance().get_tunnel_url()
    if not tunnel_url:
        return "Error: No public tunnel active. Instagram requires a public URL. Please ask to 'start tunnel' first."

    # Construct public URL for the image
    filename = os.path.basename(image_path)
    # The public_image endpoint (python/api/public_image.py) serves files from outputs/
    image_url = f"{tunnel_url}/public_image?filename={filename}"

    try:
        # Call the actual Instagram helper
        res = instagram.post_image(image_url, caption)
        if res and "id" in res:
            return f"Success! Posted to Instagram. Media ID: {res['id']}"
        else:
            return f"Failed to post to Instagram. Response: {res}"
    except Exception as e:
        return f"Error posting to Instagram: {str(e)}"


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
        prompt, options = _extract_sd_request(getattr(msg, "arguments", ""))
        if not prompt:
            error = "Stable Diffusion tool requires a 'prompt' argument."
        else:
            kwargs: Dict[str, Any] = {}
            output_dir = options.get("output_dir")
            if isinstance(output_dir, str) and output_dir.strip():
                kwargs["output_dir"] = output_dir
            seed = _coerce_int(options.get("seed"))
            if seed is not None:
                kwargs["seed"] = seed
            steps = _coerce_int(options.get("steps"))
            if steps is not None and steps > 0:
                kwargs["steps"] = steps
            guidance = _coerce_float(options.get("guidance_scale"))
            if guidance is not None and guidance >= 0:
                kwargs["guidance_scale"] = guidance
            try:
                result = _sd_generate(prompt, **kwargs)
            except Exception as exc:  # pragma: no cover - optional dependency
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
