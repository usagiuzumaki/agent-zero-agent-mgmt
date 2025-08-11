# Provide a JSON summary of given messages
- From the messages you are given, write a summary of key points in the conversation.
- Do not include the full text of the messages, just the main ideas.
- Use clear and concise language.
- Include important aspects and remove unnecessary details.
- Keep necessary information like file names, URLs, keys etc.
- Ensure the summary is easy to understand and captures the essence of the conversation.
- If the messages are too long, summarize them to save space.

# Expected output format
~~~json
{
    "system_info": "Messages have been summarized to save space.",
    "messages_summary": ["Key point 1...", "Key point 2..."]
}
~~~