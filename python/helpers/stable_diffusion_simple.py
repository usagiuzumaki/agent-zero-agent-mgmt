"""Simplified Stable Diffusion wrapper that avoids import hangs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from textwrap import dedent, indent


def _build_script(
    *,
    prompt: str,
    output_dir: str,
    negative_prompt: str | None,
    steps: int,
    guidance_scale: float,
    width: int,
    height: int,
    seed: int | None,
    model_version: str,
    api_token: str,
) -> str:
    seed_block = ""
    if seed is not None:
        seed_block = indent(
            dedent(
                f"""
                if isinstance(payload.get("input"), dict):
                    payload["input"]["seed"] = {seed}
                """
            ).strip(),
            "        ",
        )

    script = dedent(
        f"""
        import json
        import os
        import sys
        import time
        import urllib.request
        from datetime import datetime

        api_token = {json.dumps(api_token)}
        if not api_token:
            print("ERROR: REPLICATE_API_TOKEN not provided")
            sys.exit(1)

        url = "https://api.replicate.com/v1/predictions"
        headers = {{
            "Authorization": f"Bearer {{api_token}}",
            "Content-Type": "application/json"
        }}

        payload = {{
            "version": {json.dumps(model_version)},
            "input": {{
                "prompt": {json.dumps(prompt)},
                "num_inference_steps": {steps},
                "guidance_scale": {guidance_scale},
                "width": {width},
                "height": {height},
                "num_outputs": 1,
                "scheduler": "K_EULER"
            }}
        }}

        negative_prompt = {json.dumps(negative_prompt)}
        if negative_prompt:
            payload["input"]["negative_prompt"] = negative_prompt

        {seed_block}

        data = json.dumps(payload).encode()

        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            prediction = json.loads(response.read())
        except Exception as exc:  # pragma: no cover - network interaction
            print(f"ERROR: {{exc}}")
            sys.exit(1)

        prediction_id = prediction.get("id")
        if not prediction_id:
            print("ERROR: Missing prediction id")
            sys.exit(1)

        status_url = f"https://api.replicate.com/v1/predictions/{{prediction_id}}"

        for _ in range(30):
            try:
                req = urllib.request.Request(status_url, headers={{"Authorization": f"Bearer {{api_token}}"}})
                response = urllib.request.urlopen(req, timeout=10)
                result = json.loads(response.read())
            except Exception as exc:  # pragma: no cover - network interaction
                print(f"ERROR: {{exc}}")
                sys.exit(1)

            status = result.get("status")
            if status == "succeeded":
                outputs = result.get("output") or []
                if not outputs:
                    print("ERROR: Empty output from Replicate")
                    sys.exit(1)

                image_url = outputs[0]
                os.makedirs({json.dumps(output_dir)}, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join({json.dumps(output_dir)}, f"sd_image_{{timestamp}}.png")
                urllib.request.urlretrieve(image_url, filename)
                print(filename)
                sys.exit(0)

            if status == "failed":
                error = result.get("error", "Unknown error")
                print(f"ERROR: {{error}}")
                sys.exit(1)

            time.sleep(2)

        print("ERROR: Timeout waiting for image")
        sys.exit(1)
        """
    ).strip()

    return script


def generate_image(
    prompt: str,
    output_dir: str = "outputs",
    *,
    negative_prompt: str | None = None,
    steps: int = 25,
    guidance_scale: float = 7.5,
    width: int | None = None,
    height: int | None = None,
    seed: int | None = None,
    model_version: str | None = None,
) -> str:
    """Generate an image via Replicate using a subprocess helper."""

    api_token = (os.getenv("REPLICATE_API_TOKEN") or "").strip()
    if not api_token:
        raise RuntimeError("REPLICATE_API_TOKEN environment variable not set")

    width = width or 1024
    height = height or 1024
    model_version = model_version or "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"

    script = _build_script(
        prompt=prompt,
        output_dir=output_dir,
        negative_prompt=negative_prompt,
        steps=steps,
        guidance_scale=guidance_scale,
        width=width,
        height=height,
        seed=seed,
        model_version=model_version,
        api_token=api_token,
    )

    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=90,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise RuntimeError("Image generation timed out after 90 seconds") from exc

    if result.returncode == 0:
        filename = result.stdout.strip()
        if filename and os.path.exists(filename):
            return filename
        raise RuntimeError("Image generation completed but no file was produced")

    error_msg = result.stdout.strip() or result.stderr.strip()
    if error_msg.startswith("ERROR: "):
        error_msg = error_msg[7:]
    raise RuntimeError(f"Image generation failed: {error_msg or 'unknown error'}")