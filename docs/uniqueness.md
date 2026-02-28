# Aria Uniqueness Engine v1

The Uniqueness Engine is a subsystem that makes Aria feel like a singular entity with signature behaviors, rather than a generic LLM wrapper.

## Architecture

- **Engine (`AriaUniquenessEngine`):** The main orchestrator that runs the uniqueness pipeline.
- **Traits (`SignatureTrait`):** Modules that inject distinctive micro-patterns into Aria's system prompt and optionally process her responses.
- **Rituals (`Ritual`):** Repeatable, charming behaviors that trigger under specific conditions.
- **Voice (`AriaVoice`):** Re-shapes raw LLM output to match Aria's specific tone (e.g., removing boilerplate).
- **Response Shaper (`ResponseShaper`):** Ensures final output is structured and useful.
- **Memory Style (`AriaMemoryStyle`):** Customizes how and what Aria remembers.
- **Score (`UniquenessScorer`):** Measures the 'uniqueness' of each response to prevent generic drift.

## Adding New Signature Traits

1. Create a new file in `python/uniqueness/traits/` (e.g., `my_trait.py`).
2. Inherit from `SignatureTrait` and implement `get_system_prompt` and optionally `apply`.
3. Enable the trait in `python/uniqueness/uniqueness.config.json`.

## Adding New Rituals

1. Create a new file in `python/uniqueness/rituals/` (e.g., `my_ritual.py`).
2. Inherit from `Ritual` and implement `name`, `when`, and `apply`.
3. Enable the ritual in `python/uniqueness/uniqueness.config.json`.

## Configuration

The engine is controlled by `python/uniqueness/uniqueness.config.json` and a feature flag in `AgentConfig` (`uniqueness_engine=True`).
