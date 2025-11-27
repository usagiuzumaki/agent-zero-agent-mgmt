# ARIA New UI Brainstorm

## Experience goals
- Feel like a lively companion that is creative, supportive, and proactive without overwhelming the user.
- Put the chat flow first while showcasing key behaviors: creativity, coaching, investing guidance, and memory.
- Encourage users to try quick scenarios with minimal typing.
- Surface status and safety at a glance (connection, session state, current vibe).
- Maintain readability for long-form conversations.

## Visual direction
- Neon glassmorphism with soft pink–teal gradients and subtle grid lines to keep the "kawaii" vibe while staying professional.
- Floating cards with depth and animated glows to emphasize interactivity.
- Compact typography with accent pill badges for "mood" and "focus" cues.

## Layout sketch
1. **Hero band** at the top of the chat with avatar glow, tagline, and connection state.
2. **Quick prompts** as pill chips that pre-fill the chat input so users can start fast.
3. **Intent grid** with three cards: Creative Studio, Strategy Lab, Wellness Check. Each card highlights a capability and nudges a suggested action.
4. **Progress pulses** showing streaks, bookmarks, and saved ideas to remind the user of continuity.
5. **Ambient gradient background** applied to the whole app, with elevated panels for left navigation and the chat area.

## Interaction notes
- Quick prompt chips call existing `updateChatInput` and `sendMessage` to stay consistent with the backend.
- Cards are hoverable and keyboard-focusable; pressing them will insert curated starter prompts.
- The layout is responsive: hero band stacks on small screens and keeps the main chat visible.

## Implementation summary
- Added a new `aurora-theme.css` for gradients, glass cards, and typography.
- Injected a new hero and intent grid into `index.html` above the chat stream.
- Created `aurora-theme.js` to wire quick prompts and intent cards to the existing chat input pipeline.
