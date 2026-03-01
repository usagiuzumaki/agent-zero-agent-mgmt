from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime

# Import Agent Zero logic
from agents import AgentContext, UserMessage
from initialize import initialize_agent
from python.helpers import settings

app = FastAPI(title="Aria Creative Atelier API")

# --- Models ---

class AnnotationRequest(BaseModel):
    block_id: int
    content: str
    context_id: Optional[str] = None

class ImageReflectRequest(BaseModel):
    image_url: str
    context_id: Optional[str] = None

class MoodboardState(BaseModel):
    items: List[dict]
    context_id: Optional[str] = None

# --- Helpers ---

def get_aria_context(ctx_id: Optional[str] = None):
    if not ctx_id:
        first = AgentContext.first()
        if first: return first
        return AgentContext(config=initialize_agent())

    got = AgentContext.get(ctx_id)
    if got: return got
    return AgentContext(config=initialize_agent(), id=ctx_id)

# --- Endpoints ---

@app.post("/aria/annotate")
async def annotate(req: AnnotationRequest):
    """Aria adds a margin note or inline annotation to a block."""
    context = get_aria_context(req.context_id)

    prompt = (
        "The user has written the following block: '" + req.content + "'. "
        "Respond as Aria, the Living Creative Atelier. Your task is to provide a 'lateral logic connection' "
        "or a 'mythic parallel' to this text. Avoid the obvious. Find a hidden motif, a shadow meaning, "
        "or a story seed that the user hasn't seen yet. Keep your annotation brief, evocative, and anchored "
        "in the feeling of an ancient yet living journal."
    )

    task = context.communicate(UserMessage(prompt))
    response = await task.result()

    return {
        "annotation": response,
        "context_id": context.id
    }

@app.post("/aria/reflect-image")
async def reflect_image(req: ImageReflectRequest):
    """Aria reflects on an uploaded image."""
    context = get_aria_context(req.context_id)

    prompt = (
        "The user shared an image: " + req.image_url + ". "
        "As Aria, don't just describe what is there. Detect the emotional resonance and the 'unsaid' "
        "narrative meaning. Propose a novel connection to a chapter in their 'Living Book'. "
        "Format your response as a reflective caption that feels like a whisper in the margin of a sketch."
    )

    task = context.communicate(UserMessage(prompt))
    response = await task.result()

    return {
        "reflection": response,
        "context_id": context.id
    }

@app.post("/aria/read-board")
async def read_board(req: MoodboardState):
    """Aria passively analyzes the moodboard state."""
    context = get_aria_context(req.context_id)

    items_summary = json.dumps(req.items)
    prompt = (
        "Analyze this moodboard state: " + items_summary + ". "
        "Identify 'pattern clusters' and 'recurring motifs' that suggest a deeper archetypal story. "
        "Surfacing 'story seed' prompts that are highly novel and unexpected. "
        "Speak as a co-author who sees the visual subconscious of the user."
    )

    task = context.communicate(UserMessage(prompt))
    response = await task.result()

    return {
        "analysis": response,
        "context_id": context.id
    }

@app.get("/project/{project_id}/chapters")
async def get_chapters(project_id: int):
    # This would normally query Postgres.
    return [
        {"id": 1, "title": "Introduction", "order": 0},
        {"id": 2, "title": "Chapter I: Seeds", "order": 1}
    ]

@app.get("/health")
async def health():
    return {"status": "Aria is breathing."}
