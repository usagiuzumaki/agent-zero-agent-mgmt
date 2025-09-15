"""Tool exposing Stable Diffusion Colab guidance for the e-girl agent."""

from __future__ import annotations

from python.helpers.tool import Response, Tool
from python.helpers.egirl import colab as colab_helper


def _optional_int(value, *, label: str) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an integer") from exc


def _optional_float(value, *, label: str) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a number") from exc


def _optional_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "y", "on"}:
            return True
        if lowered in {"0", "false", "no", "n", "off"}:
            return False
    return False


def _first_non_empty(kwargs: dict, *keys: str):
    for key in keys:
        value = kwargs.get(key)
        if isinstance(value, str):
            value = value.strip()
        if value not in (None, ""):
            return value
    return None


class EgirlStableDiffusionColabTool(Tool):
    """Provide instructions for using the shared Stable Diffusion Colab notebook."""

    async def execute(self, **kwargs) -> Response:  # noqa: D401 - Tool protocol
        task = (kwargs.get("task") or "").strip().lower()

        try:
            if task in {"overview", "colab_overview", "summary"}:
                message = colab_helper.get_overview()
                return Response(message=message, break_loop=False)

            if task in {"workflow", "colab_workflow", "run", "guide"}:
                prompt = _first_non_empty(kwargs, "prompt", "text", "positive_prompt")
                negative_prompt = _first_non_empty(
                    kwargs, "negative_prompt", "negative"
                )
                steps = _optional_int(
                    _first_non_empty(kwargs, "steps", "num_inference_steps"),
                    label="steps",
                )
                guidance = _optional_float(
                    _first_non_empty(kwargs, "guidance", "cfg", "cfg_scale"),
                    label="guidance",
                )
                num_images = _optional_int(
                    _first_non_empty(kwargs, "num_images", "batch_count", "batch_size"),
                    label="num_images",
                )
                scheduler = _first_non_empty(
                    kwargs, "scheduler", "sampler", "sampling_method"
                )

                message = colab_helper.build_workflow(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    steps=steps,
                    guidance=guidance,
                    num_images=num_images,
                    scheduler=scheduler,
                )
                return Response(message=message, break_loop=False)

            if task in {"download", "colab_download", "fetch"}:
                filename = _first_non_empty(
                    kwargs,
                    "filename",
                    "path",
                    "relative_path",
                    "target",
                    "output",
                )
                as_zip = _optional_bool(_first_non_empty(kwargs, "as_zip", "zip"))
                message = colab_helper.build_download_instructions(
                    filename=filename,
                    as_zip=as_zip,
                )
                return Response(message=message, break_loop=False)

            supported = "overview, workflow, download"
            return Response(
                message=f"unknown task '{task or '<empty>'}', supported: {supported}",
                break_loop=False,
            )
        except ValueError as exc:
            return Response(message=f"error: {exc}", break_loop=False)
        except Exception as exc:  # pragma: no cover - defensive
            return Response(message=f"error: {exc}", break_loop=False)

