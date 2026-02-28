from typing import Dict, Any, List
import re

class UniquenessScorer:
    def __init__(self, engine_config: Dict[str, Any]):
        self.config = engine_config

    def calculate_score(self, response: str, context: Dict[str, Any], engine_state: Dict[str, Any]) -> float:
        # Weights for the algorithm
        W_TRAITS = 0.4
        W_RITUALS = 0.3
        W_STRUCTURE = 0.2
        W_GENERIC_PENALTY = 0.1

        # 1. Presence of signature traits (from engine state)
        traits_count = len(engine_state.get("active_traits", []))
        traits_score = min(traits_count / 2, 1.0) # Goal is 1-2 traits

        # 2. Ritual usage
        ritual_score = 1.0 if engine_state.get("ritual_applied") else 0.0

        # 3. Structure maintained (no ramble)
        # Simplified: length check and bullet points
        structure_score = 1.0
        if len(response) > 2000: structure_score -= 0.5
        if response.count('\n') < 2: structure_score -= 0.2

        # 4. Genericness penalty
        penalty = 0.0
        generic_patterns = [
            r"as an ai",
            r"i am a language model",
            r"how can i help",
            r"certainly",
            r"feel free to"
        ]
        for pattern in generic_patterns:
            if re.search(pattern, response.lower()):
                penalty += 0.2

        generic_score = max(0, 1.0 - penalty)

        # Weighted Average
        total_score = (
            (traits_score * W_TRAITS) +
            (ritual_score * W_RITUALS) +
            (structure_score * W_STRUCTURE) +
            (generic_score * W_GENERIC_PENALTY)
        )

        return round(total_score, 2)
