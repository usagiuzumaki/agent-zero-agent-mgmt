import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle


class CallSubordinate(VariablesPlugin):
    def get_variables(
        self, file: str, backup_dirs: list[str] | None = None
    ) -> dict[str, Any]:
        """Return available prompt profiles.

        Parameters
        ----------
        file: str
            The markdown file requesting variables. It is unused but
            required to satisfy the :class:`VariablesPlugin` interface.
        backup_dirs: list[str] | None
            Additional directories to search for prompt profiles. These are
            also unused for now but included for interface compatibility.
        """

        # collect all prompt profiles from subdirectories (_context.md file)
        profiles: list[dict[str, Any]] = []
        prompt_subdirs = files.get_subdirectories("prompts")
        for prompt_subdir in prompt_subdirs:
            try:
                context = files.read_file(
                    files.get_abs_path("prompts", prompt_subdir, "_context.md")
                )
                profiles.append({"name": prompt_subdir, "context": context})
            except Exception as e:
                PrintStyle().error(
                    f"Error loading prompt profile '{prompt_subdir}': {e}"
                )

        # in case of no profiles
        if not profiles:
            PrintStyle().error("No prompt profiles found")
            profiles = [
                {"name": "default", "context": "Default Agent-Zero AI Assistant"}
            ]

        return {"prompt_profiles": profiles}
