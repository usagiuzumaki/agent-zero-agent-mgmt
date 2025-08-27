import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle


class CallSubordinate(VariablesPlugin):
    """Plugin for populating variables in the call_subordinate tool prompt.

    The Agent‑Zero prompt system allows markdown templates to reference
    placeholders that are provided by accompanying Python plugins. When
    rendering ``agent.system.tool.call_sub.md``, this class is loaded and
    its :meth:`get_variables` method is invoked to return a mapping of
    variable names to values.  Without the correct method signature this
    plugin fails to load and produces errors like ``TypeError:
    CallSubordinate.get_variables() takes 1 positional argument but 3 were
    given``.  To satisfy the :class:`VariablesPlugin` interface we accept
    both the ``file`` and ``backup_dirs`` parameters even though they are
    currently unused.
    """

    def get_variables(
        self, file: str, backup_dirs: list[str] | None = None
    ) -> dict[str, Any]:
        """Return available agent profiles.

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
            A mapping containing the ``agent_profiles`` key with a list of
            available agent profiles.  Each profile is a dictionary with
            ``name`` and ``context`` keys.
        """
        # Collect all agent profile contexts from subdirectories of ``agents``
        profiles: list[dict[str, Any]] = []
        agent_subdirs = files.get_subdirectories("agents", exclude=["_example"])
        for agent_subdir in agent_subdirs:
            try:
                context = files.read_file(
                    files.get_abs_path("agents", agent_subdir, "_context.md")
                )
                profiles.append({"name": agent_subdir, "context": context})
            except Exception as e:
                # Log and skip any profile that fails to load rather than
                # raising; this preserves existing behaviour while providing
                # visibility into what went wrong.
                PrintStyle().error(
                    f"Error loading agent profile '{agent_subdir}': {e}"
                )

        # Provide a default profile if none were found
        if not profiles:
            profiles = [
                {"name": "default", "context": "Default Agent‑Zero AI Assistant"}
            ]

        return {"agent_profiles": profiles}
