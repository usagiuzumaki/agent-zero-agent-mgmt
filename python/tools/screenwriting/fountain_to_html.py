from python.helpers.tool import Tool, Response
import os
import tempfile
import subprocess
import shlex

class FountainToHtml(Tool):
    """Converts Fountain scripts into shareable HTML using the fountain_to_html instrument."""

    async def execute(self, script: str = "", **kwargs) -> Response:
        """
        Executes the fountain_to_html instrument.

        Args:
            script: The content of the fountain script to convert, or a path to a file.
        """
        script_path = script
        is_temp = False

        # Determine if input is a file path or content
        # If it contains newlines, it's definitely content.
        # If it doesn't verify existence.
        if "\n" in script or (not os.path.exists(script)):
             # Treat as content
             with tempfile.NamedTemporaryFile(mode='w', suffix='.fountain', delete=False, encoding='utf-8') as tmp:
                 tmp.write(script)
                 script_path = tmp.name
                 is_temp = True

        # Path to the instrument script
        instrument_path = os.path.join("instruments", "default", "fountain_to_html", "fountain_to_html.py")

        # Use subprocess with list args to avoid shell injection
        cmd = ["python3", instrument_path, script_path]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            output = result.stdout
            if result.stderr:
                # If there's stderr, append it but don't fail, as some tools print warnings to stderr
                output += f"\nStderr: {result.stderr}"
        except Exception as e:
            output = f"Error executing tool: {str(e)}"
        finally:
            if is_temp and os.path.exists(script_path):
                os.remove(script_path)

        return Response(message=output, break_loop=False)
