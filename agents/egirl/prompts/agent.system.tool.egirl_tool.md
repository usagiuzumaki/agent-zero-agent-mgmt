### egirl_tool:
- Use `task: post_instagram` with `image_url` and `caption` to publish a picture.
- Use `task: comment_instagram` with `hashtags`, `text`, and optional `max_posts` to comment on posts.
- Use `task: generate_image` with `prompt` and optional `output_dir` to create an image via Stable Diffusion.
- Use `task: generate_video` with `image_path`, `prompt`, and optional `output_path` to create a short clip.
- Use `task: generate_voice` with `text` and optional `output_path` for ElevenLabs text-to-speech.
- Use `task: stripe_payment` with `price_id` to create a Stripe checkout link.
- Use `task: stripe_subscription` with `price_id` to start a subscription.
- Use `task: stripe_refund` with `payment_intent` to refund a payment.
- Use `task: stripe_payout` with `amount` and optional `currency` to issue a payout.
- Use `task: persona_chat` with `message` and optional `name` for a stylized reply.

**Example usage**:
~~~json
{
    "thoughts": ["..."] ,
    "tool_name": "egirl_tool",
    "tool_args": {
        "task": "post_instagram",
        "image_url": "https://example.com/image.jpg",
        "caption": "hello"
    }
}
~~~
