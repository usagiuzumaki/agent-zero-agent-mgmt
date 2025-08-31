from python.helpers.tool import Tool, Response

class EgirlTool(Tool):
    async def execute(self, **kwargs) -> Response:
        task = kwargs.get("task")
        try:
            if task == "post_instagram":
                from python.helpers.egirl.instagram import post_image
                image_url = kwargs.get("image_url", "")
                caption = kwargs.get("caption", "")
                res = post_image(image_url, caption)
                return Response(message=str(res), break_loop=False)
            if task == "comment_instagram":
                from python.helpers.egirl.instagram import comment_on_hashtags
                tags = kwargs.get("hashtags", [])
                text = kwargs.get("text", "")
                max_posts = kwargs.get("max_posts", 3)
                comment_on_hashtags(tags, text, max_posts)
                return Response(message="comments attempted", break_loop=False)
            if task == "generate_image":
                from python.helpers.stable_diffusion import generate_image
                import os
                prompt = kwargs.get("prompt", "")
                # allow either output_dir or legacy output_path argument
                output_dir = kwargs.get("output_dir")
                if not output_dir:
                    output_path = kwargs.get("output_path", "outputs")
                    output_dir = os.path.dirname(output_path) or "outputs"
                path = generate_image(prompt, output_dir=output_dir)
                return Response(message=f"generated {path}", break_loop=False)
            if task == "generate_video":
                from python.helpers.egirl.video import generate_video_from_image
                image_path = kwargs.get("image_path")
                prompt = kwargs.get("prompt", "")
                output_path = kwargs.get("output_path", "outputs/video.mp4")
                path = generate_video_from_image(image_path, prompt, output_path)
                return Response(message=f"video at {path}", break_loop=False)
            if task == "generate_voice":
                from python.helpers.egirl.elevenlabs import text_to_speech
                text = kwargs.get("text", "")
                output_path = kwargs.get("output_path", "outputs/egirl_tts.mp3")
                path = text_to_speech(text, output_path)
                return Response(message=f"voice at {path}" if path else "voice generation failed", break_loop=False)
            if task in ("stripe_checkout", "stripe_payment"):
                from python.helpers.egirl.stripe import create_checkout_session
                price_id = kwargs.get("price_id", "")
                url = create_checkout_session(price_id, kwargs.get("success_url"), kwargs.get("cancel_url"))
                return Response(message=url or "", break_loop=False)
            if task == "stripe_subscription":
                from python.helpers.egirl.stripe import create_subscription_session
                price_id = kwargs.get("price_id", "")
                url = create_subscription_session(price_id, kwargs.get("success_url"), kwargs.get("cancel_url"))
                return Response(message=url or "", break_loop=False)
            if task == "stripe_refund":
                from python.helpers.egirl.stripe import create_refund
                payment_intent = kwargs.get("payment_intent", "")
                refund_id = create_refund(payment_intent)
                return Response(message=refund_id or "", break_loop=False)
            if task == "stripe_payout":
                from python.helpers.egirl.stripe import create_payout
                amount = kwargs.get("amount")
                currency = kwargs.get("currency", "usd")
                payout_id = create_payout(amount, currency)
                return Response(message=payout_id or "", break_loop=False)
            if task == "persona_chat":
                from python.helpers.egirl.persona import PersonaEngine
                name = kwargs.get("name", "Aria")
                msg = kwargs.get("message", "")
                persona = PersonaEngine(name)
                result = persona.generate_response(msg)
                message = result.get("text", "")
                if result.get("audio_path"):
                    message += f" (audio: {result['audio_path']})"
                if result.get("tool_result"):
                    message += f" (result: {result['tool_result']})"
                return Response(message=message, break_loop=False)
        except Exception as e:
            return Response(message=f"error: {e}", break_loop=False)
        return Response(message="unknown task", break_loop=False)
