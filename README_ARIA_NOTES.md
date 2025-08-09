
# Aria Bot Merge Notes
- UI rebrand: 'Agent Zero' -> 'Aria Bot' where found.
- Added instruments: Stripe, Instagram, ElevenLabs, Stable Diffusion (each with run.sh).
- instruments.py import stubs added.
- agent/egirl/ persona folder added (prompt.md if missing).
- main.py loads persona prompt.
- Dockerfile: please ensure deps installed (stripe, requests, elevenlabs, or diffusers stack).
- Secrets: DO NOT COMMIT .env. Set at runtime.
