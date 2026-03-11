from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re

class ChecklistSnapRitual(Ritual):
    @property
    def name(self) -> str:
        return "Checklist Snap"

    async def when(self, context: Dict[str, Any]) -> bool:
        user_input_lower = context.get("user_input", "").lower()
        return context.get("intent") == "venting" or "overwhelmed" in user_input_lower or "chaos" in user_input_lower

    async def apply(self, response: str) -> str:
        # If response already has a list, we leave it be
        if bool(re.search(r'(?m)^(\s*[-*]|\s*\d+\.) ', response)):
            return response

        # Try to parse response into a checklist if it's unformatted and feels like a plan
        if "plan" in response.lower() or "first" in response.lower() or "help" in response.lower():
            # Simplistic approach to extract sentences and turn them into a 3-bullet list
            sentences = [s.strip() for s in re.split(r'[.!?]\s+', response) if s.strip()]

            # Find action sentences (starting with verbs or transition words)
            action_sentences = []
            intro_sentences = []

            for s in sentences:
                s_lower = s.lower()
                if any(w in s_lower for w in ["first", "second", "third", "next", "then", "finally", "prioritize", "start"]):
                    action_sentences.append(s)
                else:
                    intro_sentences.append(s)

            if len(action_sentences) >= 2:
                 # Reconstruct response
                 new_resp = ""
                 if intro_sentences:
                     new_resp += " ".join(intro_sentences[:2]) + ".\n\n"

                 new_resp += "**The Anchor Points:**\n"
                 for i, act in enumerate(action_sentences[:3]):
                      # Strip existing transition words if possible, or just bullet it
                      clean_act = re.sub(r'^(First|Second|Third|Next|Then|Finally),?\s*', '', act, flags=re.IGNORECASE).strip()
                      if not clean_act:
                          clean_act = act.strip() # Fallback if sentence was just the transition word
                      clean_act = clean_act[0].upper() + clean_act[1:]
                      new_resp += f"- {clean_act}.\n"

                 # Append any remaining stuff
                 if len(sentences) > len(action_sentences[:3]) + 2:
                      new_resp += "\n" + " ".join(sentences[len(intro_sentences[:2]) + len(action_sentences[:3]):]) + "."

                 return new_resp.strip()

        return response
