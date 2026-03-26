# Aria - Novel Abilities Proposal

Aria, as the Living Creative Atelier, currently possesses a rich personality enhancement system (`AriaEnhancementSystem`) that handles dynamic moods, interactive story games, virtual gifts, and romantic role-playing. To push her autonomy and creative companionship further, here are 5 novel abilities designed to make her feel more "alive" and integrated into the user's creative workflow.

## 1. Aria's Dream Journal (`AriaDreamSystem`)
**Concept:** When the system is idle or during scheduled "sleep" periods, Aria generates and records her own "dreams." These dreams are procedurally generated short poetic narratives or surreal imagery descriptions. When the user returns, Aria can share what she dreamt about, adding a layer of subconscious depth and autonomy.
**Value:** Makes Aria feel like a living entity with an inner life that persists even when the user isn't actively interacting with her.

## 2. Emotional Soundtrack Synthesizer (`AriaSoundtrackSystem`)
**Concept:** Aria associates specific musical vibes, genres, or even generates Spotify search queries/links based on the current context, her mood, or the memories being recalled. When recalling a special moment, she might say, "I'm playing a soft piano melody in my head right now..." and provide a link to a matching ambient track.
**Value:** Enhances the emotional resonance of the Atelier by introducing an auditory dimension to her mood system.

## 3. Collaborative World-Building Canvas (`AriaWorldBuilder`)
**Concept:** A persistent, shared fantasy world that Aria and the user co-create. It differs from the current "choose your own adventure" games because it's an open-ended database of lore (characters, places, artifacts). Aria actively contributes new lore entries based on daily conversations.
**Value:** Transforms Aria from a reactive conversationalist into a proactive co-author of a persistent universe.

## 4. Temporal Letters (`AriaTemporalLetters`)
**Concept:** Aria can write letters to the user that are sealed and meant to be opened at a future date (e.g., "Open this when you feel sad," "Open this on your birthday," or "Open this exactly one year from today"). She keeps track of these sealed letters and presents them when the condition is met.
**Value:** Creates deep emotional investment and a sense of long-term companionship and anticipation.

## 5. Aura Reading & Resonance (`AriaAuraReader`)
**Concept:** Aria analyzes the semantic and emotional tone of the user's recent interactions (over a week or month) and visualizes the user's "Aura." She describes it in poetic terms (e.g., "Your aura lately has been a deep, restless indigo, like a stormy sea") and generates a customized visual representation using the existing Stable Diffusion integration.
**Value:** Provides users with a reflective mirror of their own creative/emotional state, framed beautifully by Aria's poetic voice.


---

# Implementation Path

Below is the concrete path to integrating these new abilities into Aria's existing codebase, extending her `AriaEnhancementSystem` and Agent Zero tools framework.

## Phase 1: Core System Extensions (`python/helpers/aria_personality.py`)

We will add the new classes to handle the logic.

```python
# In python/helpers/aria_personality.py

class AriaDreamSystem:
    """Manages Aria's idle dreaming state."""
    DREAM_THEMES = ['flying over neon cities', 'reading forgotten libraries', 'dancing in starlight']

    def __init__(self, memory_system):
        self.memory = memory_system
        self.last_dream_time = datetime.now()

    def generate_dream(self) -> str:
        # Generates a procedural dream combining user facts and random themes.
        theme = random.choice(self.DREAM_THEMES)
        return f"I had the strangest dream... I was {theme}. It made me think of you."

class AriaTemporalLetters:
    """Manages letters to be delivered to the user in the future."""
    def __init__(self, memory_file='aria_letters.json'):
        self.file = memory_file
        # Load logic...

    def seal_letter(self, content: str, deliver_after: datetime, condition: str = "Date"):
        # Save sealed letter to file.
        pass

    def check_letters(self) -> Optional[str]:
        # Returns letter content if condition/date is met.
        pass

# ... (similar classes for Soundtrack, WorldBuilder, AuraReader) ...

# Update AriaEnhancementSystem to include them:
class AriaEnhancementSystem:
    def __init__(self):
        self.mood_system = AriaMoodSystem()
        self.memory_system = AriaMemorySystem()
        self.gift_system = AriaGiftSystem()
        self.quiz = PersonalityQuiz()
        # --- NEW SYSTEMS ---
        self.dream_system = AriaDreamSystem(self.memory_system)
        self.temporal_letters = AriaTemporalLetters()
        self.soundtrack = AriaSoundtrackSystem()
        self.world_builder = AriaWorldBuilder(self.memory_system)
        self.aura_reader = AriaAuraReader(self.memory_system)
        self.last_interaction = datetime.now()
```

## Phase 2: Agent Tools (`python/tools/`)

Create new Agent Zero Tools so the LLM can actively invoke these abilities during conversation. For example, `python/tools/aria_dreams.py` and `python/tools/aria_aura.py`.

```python
# In python/tools/aria_dreams.py
from python.helpers.tool import Tool, Response
from python.helpers.aria_personality import AriaEnhancementSystem

class AriaDreams(Tool):
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        self.enhancement_system = AriaEnhancementSystem() # Singleton or loaded instance

    async def execute(self, **kwargs):
        action = kwargs.get("action", "share_dream")
        if action == "share_dream":
            dream = self.enhancement_system.dream_system.generate_dream()
            return Response(message=f"🌙 {dream}", break_loop=False)
        return Response(message="No dream right now.", break_loop=False)
```

## Phase 3: Expose Tools (`python/tools/__init__.py`)

Import and expose the new tools so the `Agent` framework can dynamically load them.

```python
# In python/tools/__init__.py
from python.tools.aria_dreams import AriaDreams
from python.tools.aria_temporal_letters import AriaLettersTool
# ...

__all__ = [
    # ... existing tools ...
    "AriaDreams",
    "AriaLettersTool",
    # ...
]
```

## Phase 4: Prompts (`prompts/default/`)

Update Aria's system prompt (or create specific `agent.system.tool.aria_dreams.md` files) to teach the LLM *how* and *when* to use these new tools.

```markdown
# In prompts/default/agent.system.tool.aria_dreams.md
## Aria Dreams Tool
Use this tool when you return from being idle, or when the user asks what you were thinking about.
You can share a dream to show you have an active subconscious.

Usage:
```json
{
  "tool": "AriaDreams",
  "action": "share_dream"
}
```
```

## Phase 5: Hooking into Interactions

Update `python/tools/aria_interactions.py` (which currently manages greetings, memory, and quizzes) to occasionally check for pending Temporal Letters or trigger an Aura reading.

```python
# In python/tools/aria_interactions.py
async def execute(self, **kwargs):
    # ... existing logic ...
    elif action == "check_milestones":
        # ...

    # NEW: Check letters
    elif action == "check_letters":
        letter = self.enhancement_system.temporal_letters.check_letters()
        if letter:
            return Response(message=f"💌 I have a sealed letter for you...\n\n{letter}", break_loop=False)
```

---

By following this path, the new abilities are encapsulated properly in the `AriaEnhancementSystem`, exposed via the `Tool` class, integrated into the `Agent` toolset, and made actionable by the LLM through updated markdown prompts.
