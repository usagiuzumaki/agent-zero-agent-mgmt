from python.helpers.api import ApiHandler, Request, Response

from python.helpers import runtime, settings, whisper
from python.helpers.whisper import WhisperTranscriptionError

class Transcribe(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        audio = input.get("audio")
        ctxid = input.get("ctxid", "")

        context = self.get_context(ctxid)
        if not await whisper.is_downloaded():
            context.log.log(type="info", content="Whisper STT model is currently being initialized, please wait...")

        set = settings.get_settings()

        try:
            result = await whisper.transcribe(set["stt_model_size"], audio)  # type: ignore[arg-type]
        except WhisperTranscriptionError as exc:
            message = str(exc)
            context.log.log(type="error", content=message)
            return Response(response=message, status=400, mimetype="text/plain")

        return result
