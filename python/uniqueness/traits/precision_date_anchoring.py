from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
from datetime import datetime, timedelta
import re

class PrecisionDateAnchoringTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return (
            "Signature Trait: Precision Date Anchoring. "
            f"Always anchor time-based references to concrete dates. Current date is {current_date}. "
            "If the user says 'next week', refer to the specific dates. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # Regex to find vague time terms and append precision dates to them in parentheses
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        tomorrow_str = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        next_week_str = (now + timedelta(days=7)).strftime("%Y-%m-%d")

        # We only want to add the parenthetical if it's not already there.
        # Simplistic approach: just find standalone "today", "tomorrow" etc and replace.
        # This regex ensures we only match whole words and we don't duplicate.

        replacements = [
            (r'(?i)\b(today)\b(?!\s*\()', f"\\1 ({today_str})"),
            (r'(?i)\b(tomorrow)\b(?!\s*\()', f"\\1 ({tomorrow_str})"),
            (r'(?i)\b(yesterday)\b(?!\s*\()', f"\\1 ({yesterday_str})"),
            (r'(?i)\b(next week)\b(?!\s*\()', f"\\1 (starting {next_week_str})")
        ]

        for pattern, replacement in replacements:
            draft_response = re.sub(pattern, replacement, draft_response)

        return draft_response
