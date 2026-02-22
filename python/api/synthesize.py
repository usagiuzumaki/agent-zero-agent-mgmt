# api/synthesize.py

from python.helpers.api import ApiHandler, Request, Response
from python.helpers import kokoro_tts

class Synthesize(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        text = input.get("text", "")
        ctxid = input.get("ctxid", "")

        context = self.get_context(ctxid)
        if not await kokoro_tts.is_downloaded():
            context.log.log(type="info", content="Kokoro TTS model is currently being initialized, please wait...")

        try:
            # audio is chunked on the frontend for better flow
            audio = await kokoro_tts.synthesize_sentences([text])
            return {"audio": audio, "success": True}
        except Exception as e:
            context.log.log(type="error", content=f"TTS Error: {str(e)}")
            return {"error": str(e), "success": False}
