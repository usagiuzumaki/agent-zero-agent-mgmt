import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle


class CallSubordinate(VariablesPlugin):
    """Plugin for populating variables in the egirl call_subordinate tool prompt.

    Unlike the global call_subordinate plugin that looks up agent profiles,
    this variant searches within the ``prompts`` directory to build a list
    of prompt profiles.  It accepts the ``file`` and ``backup_dirs``
    arguments for compatibility with the :class:`VariablesPlugin` interface.
    """

    def get_variables(
        self, file: str, backup_dirs: list[str] | None = None
    ) -> dict[str, Any]:
        """Return available prompt profiles for egirl agent.

        Parameters
        ----------
        file : str
            The markdown file requesting variables.  It is unused but
            required to satisfy the :class:`VariablesPlugin` interface.
        backup_dirs : list[str] | None
            Additional directories to search for prompt profiles.  These are
            unused for now but included for interface compatibility.

        Returns
        -------
        dict[str, Any]
            A mapping containing the ``prompt_profiles`` key with a list of
            available prompt profiles.  Each profile is a dictionary with
            ``name`` and ``context`` keys.
        """
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

        if not profiles:
            # Log and provide a default profile to avoid empty lists
            PrintStyle().error("No prompt profiles found")
            profiles = [
                {"name": "default", "context": "Default Agent‑Zero AI Assistant"}
            ]

        return {"prompt_profiles": profiles}
