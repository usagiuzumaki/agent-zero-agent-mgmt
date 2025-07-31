from pathlib import Path
import re
from python.helpers.tool import Tool, Response

MANUAL_PATH = (
    Path(__file__).resolve().parents[2]
    / "instruments"
    / "custom"
    / "screenwriting_team"
    / "screenwriting_team.md"
)


COMMAND_HEADERS = {
    "developmental edit": "Developmental Edit",
    "line edit": "Line Edit",
    "copy edit": "Copy Edit",
    "proofread": "Proofread",
    "character overview": "Character Overview",
    "plot overview": "Plot Overview",
    "analyse character": "Analyse Character",
    "analyse story structure": "Analyse Story Structure",
    "identify plotholes": "Identify Plot Holes",
}


def _extract_section(manual: str, header: str) -> str:
    pattern = rf"^##\s+{re.escape(header)}\s*$"
    start_match = re.search(pattern, manual, flags=re.MULTILINE)
    if not start_match:
        return manual
    start = start_match.start()
    next_match = re.search(r"^##\s+", manual[start + 1 :], flags=re.MULTILINE)
    end = start + 1 + next_match.start() if next_match else len(manual)
    return manual[start:end].strip()


class ScreenwritingTeam(Tool):
    async def execute(self, command="help", **kwargs):
        manual = MANUAL_PATH.read_text(encoding="utf-8")
        cmd = command.strip().lower()
        if cmd in {"help", "rtfm", "manual"}:
            return Response(message=manual, break_loop=False)
        header = COMMAND_HEADERS.get(cmd)
        if header:
            section = _extract_section(manual, header)
            return Response(message=section, break_loop=False)
        known = ", ".join(sorted(COMMAND_HEADERS.keys()))
        return Response(
            message=f"Unknown command '{command}'. Available commands: {known}.",
            break_loop=False,
        )
