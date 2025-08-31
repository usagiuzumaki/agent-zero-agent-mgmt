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
]

# allowed tool groupings
ALLOWED_IMAGE = [{"type": "custom", "name": "sd_image"}]
ALLOWED_TTS = [{"type": "custom", "name": "eleven_tts"}]
ALLOWED_INSTAGRAM = [{"type": "function", "name": "post_to_instagram"}]

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
    if name == "sd_image":
        prompt = getattr(msg, "arguments", "")
        result = _sd_generate(prompt)
    elif name == "eleven_tts":
        text = getattr(msg, "arguments", "")
        result = _eleven_tts(text)
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
    else:
        return msg, None

    followup = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "tool",
                "content": json.dumps({"result": result}),
                "tool_call_id": getattr(msg, "id", ""),
            }
        ],
        previous_response_id=getattr(msg, "response_id", None),
    )
    return followup, result
