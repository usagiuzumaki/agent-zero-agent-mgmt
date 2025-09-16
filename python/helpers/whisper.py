"""Utilities for working with Whisper speech-to-text models."""

from __future__ import annotations

import asyncio
import base64
import binascii
import os
import tempfile
import warnings
from typing import Any

import whisper

from python.helpers import files, runtime, rfc, settings
from python.helpers.print_style import PrintStyle

try:  # pragma: no cover - PyAV is optional in some deployments
    from av.error import InvalidDataError as PyAVInvalidDataError
except Exception:  # pragma: no cover - fallback when PyAV isn't installed
    PyAVInvalidDataError = None


class WhisperTranscriptionError(RuntimeError):
    """Raised when Whisper fails to transcribe an audio recording."""


# Suppress FutureWarning from torch.load
warnings.filterwarnings("ignore", category=FutureWarning)


_model: Any | None = None
_model_name = ""
is_updating_model = False  # Tracks whether the model is currently updating


async def preload(model_name: str):
    try:
        # return await runtime.call_development_function(_preload, model_name)
        return await _preload(model_name)
    except Exception as exc:  # pragma: no cover - parity with previous behaviour
        # if not runtime.is_development():
        raise exc


async def _preload(model_name: str):
    global _model, _model_name, is_updating_model

    while is_updating_model:
        await asyncio.sleep(0.1)

    try:
        is_updating_model = True
        if not _model or _model_name != model_name:
            PrintStyle.standard(f"Loading Whisper model: {model_name}")
            _model = whisper.load_model(  # type: ignore[assignment]
                name=model_name,
                download_root=files.get_abs_path("/tmp/models/whisper"),
            )
            _model_name = model_name
    finally:
        is_updating_model = False


async def is_downloading():
    # return await runtime.call_development_function(_is_downloading)
    return _is_downloading()


def _is_downloading():
    return is_updating_model


async def is_downloaded():
    try:
        # return await runtime.call_development_function(_is_downloaded)
        return _is_downloaded()
    except Exception as exc:  # pragma: no cover - parity with previous behaviour
        # if not runtime.is_development():
        raise exc
        # Fallback to direct execution if RFC fails in development
        # return _is_downloaded()


def _is_downloaded():
    return _model is not None


async def transcribe(model_name: str, audio_bytes_b64: str):
    # return await runtime.call_development_function(_transcribe, model_name, audio_bytes_b64)
    return await _transcribe(model_name, audio_bytes_b64)


async def _transcribe(model_name: str, audio_bytes_b64: str):
    await _preload(model_name)

    if not audio_bytes_b64:
        raise WhisperTranscriptionError(
            "No audio data was provided for transcription."
        )

    try:
        audio_bytes = base64.b64decode(audio_bytes_b64)
    except (binascii.Error, TypeError) as exc:
        raise WhisperTranscriptionError(
            "Unable to decode the provided audio recording."
        ) from exc

    if not audio_bytes:
        raise WhisperTranscriptionError("The provided audio recording is empty.")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
        audio_file.write(audio_bytes)
        temp_path = audio_file.name

    try:
        if _model is None:
            raise WhisperTranscriptionError("The Whisper model is not loaded.")

        try:
            result = _model.transcribe(temp_path, fp16=False)  # type: ignore[call-arg]
        except ValueError as exc:
            if "max() arg is an empty sequence" in str(exc):
                raise WhisperTranscriptionError(
                    "Failed to detect any speech in the recording. Please try again with a clearer input."
                ) from exc
            raise
        except Exception as exc:  # pragma: no cover - unexpected backend error
            if PyAVInvalidDataError and isinstance(exc, PyAVInvalidDataError):
                raise WhisperTranscriptionError(
                    "Failed to process the recording. The audio file appears to be corrupted or in an unsupported format."
                ) from exc
            raise WhisperTranscriptionError(
                "Unexpected error while transcribing the recording."
            ) from exc

        return result
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass  # ignore errors during cleanup
