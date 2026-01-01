### egirl_sd_colab_tool:
- Use `task: overview` (aliases: `summary`, `colab_overview`) to recall the shared Stable Diffusion Colab link and the workspace layout on Google Drive.
- Use `task: workflow` (aliases: `run`, `guide`, `colab_workflow`) with optional `prompt`, `negative_prompt`, `steps`, `guidance`, `num_images`, or `scheduler` values to get the full step-by-step plan for launching the notebook and running txt2img inside AUTOMATIC1111.
- Use `task: download` (aliases: `fetch`, `colab_download`) with optional `filename`/`path` and boolean `as_zip` to receive ready-to-run snippets that download images or folders from the Colab runtime.
- Use `task: browser_prompt` (aliases: `automate`, `browser_plan`) with `prompt` (and optional parameters) to generate a detailed instruction set for the `browser_agent`. This allows you to autonomously drive the Colab notebook.

**Example usage**:
~~~json
{
    "thoughts": ["Open the shared Colab, generate an image, then download it."],
    "tool_name": "egirl_sd_colab_tool",
    "tool_args": {
        "task": "workflow",
        "prompt": "ultra-detailed portrait of an egirl hacker",
        "negative_prompt": "low quality, blurry",
        "steps": 30,
        "guidance": 7.5,
        "num_images": 2
    }
}
~~~

To automate the process yourself:
1. Call `egirl_sd_colab_tool` with `task: browser_prompt` and your desired prompt.
2. Take the returned instruction text.
3. Call `browser_agent` with the instruction text as the `message`.

To download a finished render:
~~~json
{
    "thoughts": ["Pull down the best render for posting."],
    "tool_name": "egirl_sd_colab_tool",
    "tool_args": {
        "task": "download",
        "filename": "2024-09-15/00012.png"
    }
}
~~~

