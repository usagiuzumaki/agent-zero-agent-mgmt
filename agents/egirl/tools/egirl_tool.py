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
                from python.helpers.egirl.dreambooth import generate_persona_image
                prompt = kwargs.get("prompt", "")
                output_path = kwargs.get("output_path", "outputs/persona.png")
                path = generate_persona_image(prompt, output_path)
                return Response(message=f"generated {path}", break_loop=False)
            if task == "generate_video":
                from python.helpers.egirl.video import generate_video_from_image
                image_path = kwargs.get("image_path")
                prompt = kwargs.get("prompt", "")
                output_path = kwargs.get("output_path", "outputs/video.mp4")
                path = generate_video_from_image(image_path, prompt, output_path)
                return Response(message=f"video at {path}", break_loop=False)
            if task == "stripe_checkout":
                from python.helpers.egirl.stripe import create_checkout_session
                price_id = kwargs.get("price_id", "")
                url = create_checkout_session(price_id, kwargs.get("success_url"), kwargs.get("cancel_url"))
                return Response(message=url or "", break_loop=False)
            if task == "persona_chat":
                from python.helpers.egirl.persona import PersonaEngine
                name = kwargs.get("name", "Aria")
                msg = kwargs.get("message", "")
                persona = PersonaEngine(name)
                reply = persona.generate_response(msg)
                return Response(message=str(reply), break_loop=False)
        except Exception as e:
            return Response(message=f"error: {e}", break_loop=False)
        return Response(message="unknown task", break_loop=False)
