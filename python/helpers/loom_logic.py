from typing import List, Optional

def compute_entropy(current_entropy: float, novelty: float, pattern_repeat_48h: bool) -> float:
    """
    Update each user message:
    entropy += 0.08 if novelty < 0.3
    entropy -= 0.06 if novelty > 0.6
    entropy += 0.10 if the same PatternEcho type repeats within 48h
    Clamp 0..1
    """
    new_entropy = current_entropy
    if novelty < 0.3:
        new_entropy += 0.08
    if novelty > 0.6:
        new_entropy -= 0.06
    if pattern_repeat_48h:
        new_entropy += 0.10
    return max(0.0, min(1.0, new_entropy))

def calculate_meaningfulness(narrative_weight: float, novelty: float, entropy: float) -> float:
    """
    meaningfulness = 0.5*narrative_weight + 0.3*novelty + 0.2*(1-entropy)
    """
    return 0.5 * narrative_weight + 0.3 * novelty + 0.2 * (1.0 - entropy)

def decide_mt_gate(meaningfulness: float, narrative_weight: float, utility_flag: bool, mask_conflict: bool, self_sabotage: bool, active_mask: str = 'light') -> str:
    """
    MT gate mapping:
    - Light Aria: Higher threshold for silence, more likely to reply.
    - Dark Aria: More indirect, higher threshold for direct reply, more silences/delays.

    if meaningfulness < (0.25 if light else 0.4) -> silence
    if utility_flag == true && narrative_weight < 0.5 -> refuse
    if masks disagree strongly -> delay
    if meaningfulness > 0.75 AND (self_sabotage OR dark) -> confront/indirect
    else -> reply
    """
    silence_threshold = 0.25 if active_mask == 'light' else 0.4

    if meaningfulness < silence_threshold:
        return "silence"
    if utility_flag and narrative_weight < 0.5:
        return "refuse"
    if mask_conflict:
        return "delay"

    # Dark Aria is more likely to confront or be indirect
    if active_mask == 'dark' and meaningfulness > 0.6:
        return "confront"

    if meaningfulness > 0.75 and self_sabotage:
        return "confront"

    return "reply"

def calculate_narrative_weight(
    has_desire_fear_confession: bool = False,
    references_past: bool = False,
    is_decision_point: bool = False,
    is_identity_statement: bool = False
) -> float:
    """
    narrative_weight (0–1)
    Start at 0.2
    Add +0.2 if: contains a desire/fear/confession
    Add +0.2 if: references past events
    Add +0.2 if: decision point (“I’m about to…”, “should I…”, “I can’t stop…”)
    Add +0.2 if: identity statement (“I always…”, “I’m the kind of…”)
    Clamp to 1.0
    """
    weight = 0.2
    if has_desire_fear_confession:
        weight += 0.2
    if references_past:
        weight += 0.2
    if is_decision_point:
        weight += 0.2
    if is_identity_statement:
        weight += 0.2
    return min(1.0, weight)
