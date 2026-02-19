from python.helpers.api import ApiHandler, Request, Response
from flask import jsonify

try:
    from flask_login import current_user
    from python.api.auth.trial_manager import TrialManager
    _trial_management_available = True
except ImportError:
    _trial_management_available = False


class TrialStatus(ApiHandler):
    """API endpoint to get current user's trial status"""
    
    async def process(self, input: dict, request: Request) -> dict | Response:
        if not _trial_management_available:
            return jsonify({
                "error": "Trial management not available"
            }), 503
        
        # Check if user is authenticated
        if not current_user.is_authenticated:
            return jsonify({
                "authenticated": False,
                "message": "Not authenticated",
                "redirect": "/login"
            }), 401
        
        # Get trial info for the current user
        trial_info = TrialManager.get_trial_info(current_user)
        
        return jsonify({
            "authenticated": True,
            "user_id": current_user.id,
            "email": current_user.email,
            "has_paid": current_user.has_paid,
            "trial_status": trial_info["status"],
            "remaining_seconds": trial_info["remaining_seconds"],
            "message": trial_info["message"]
        })
    
    @classmethod
    def requires_auth(cls) -> bool:
        return False  # We handle auth internally
    
    @classmethod
    def requires_csrf(cls) -> bool:
        return False  # This is a GET endpoint