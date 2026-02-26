from agents import AgentContext
from python.helpers.api import ApiHandler, Request, Response
from flask import jsonify

class JournalGet(ApiHandler):
    """
    API endpoint to retrieve Aria's daily reflections.
    Gated by MVL resonance (meaningfulness >= 0.7).
    """
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]

    async def process(self, input: dict, request: Request) -> dict | Response:
        ctxid = input.get("context") or request.args.get("context")
        if not ctxid:
             # Try to get the first context if none provided
             context = AgentContext.first()
        else:
             context = AgentContext.get(ctxid)

        if not context:
            return jsonify({"error": "Context not found"}), 404

        agent = context.get_agent()
        user_id = context.user_id

        if not hasattr(agent, "journal") or not hasattr(agent, "mvl"):
            return jsonify({"error": "Journaling system not available"}), 501

        if agent.journal.can_share_thoughts(agent.mvl, user_id):
            thoughts = agent.journal.get_todays_thoughts()
            return {
                "thoughts": thoughts,
                "allowed": True,
                "resonance": agent.journal.get_comfort_level(agent.mvl, user_id)
            }
        else:
            comfort = agent.journal.get_comfort_level(agent.mvl, user_id)
            return jsonify({
                "error": "Access denied. Resonance too low.",
                "allowed": False,
                "resonance": comfort,
                "required": 0.7
            }), 403
