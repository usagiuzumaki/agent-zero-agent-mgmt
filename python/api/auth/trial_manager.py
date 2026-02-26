from datetime import datetime, timedelta
from flask import jsonify
from flask_login import current_user
from auth_models import db

TRIAL_DURATION_MINUTES = 3  # 3-minute trial period

class TrialManager:
    """Manages user trial periods for the chat system"""
    
    @staticmethod
    def check_trial_status(user):
        """
        Check if user is within trial period or needs to pay.
        Returns: (is_allowed, remaining_seconds, message)
        """
        # If user has paid, they have full access
        if user.has_paid:
            return True, -1, "Full access"
        
        # If trial hasn't started yet, start it now
        if not user.trial_start_time:
            user.trial_start_time = datetime.utcnow()
            db.session.commit()
            return True, TRIAL_DURATION_MINUTES * 60, "Trial started"
        
        # Calculate time elapsed since trial started
        now = datetime.utcnow()
        elapsed = now - user.trial_start_time
        trial_duration = timedelta(minutes=TRIAL_DURATION_MINUTES)
        
        # Check if trial has expired
        if elapsed >= trial_duration:
            # Mark trial as expired if not already marked
            if not user.trial_expired:
                user.trial_expired = True
                db.session.commit()
            return False, 0, "Trial expired - payment required"
        
        # Trial is still active, calculate remaining time
        remaining_seconds = int((trial_duration - elapsed).total_seconds())
        return True, remaining_seconds, f"Trial active - {remaining_seconds} seconds remaining"
    
    @staticmethod
    def reset_trial(user):
        """Reset trial for a user (used after payment)"""
        user.trial_start_time = None
        user.trial_expired = False
        db.session.commit()
    
    @staticmethod
    def get_trial_info(user):
        """Get detailed trial information for frontend display"""
        if user.has_paid:
            return {
                "status": "paid",
                "remaining_seconds": -1,
                "message": "Full access - thank you for your payment!"
            }
        
        if not user.trial_start_time:
            return {
                "status": "not_started",
                "remaining_seconds": TRIAL_DURATION_MINUTES * 60,
                "message": "3-minute free trial available"
            }
        
        now = datetime.utcnow()
        elapsed = now - user.trial_start_time
        trial_duration = timedelta(minutes=TRIAL_DURATION_MINUTES)
        
        if elapsed >= trial_duration:
            return {
                "status": "expired",
                "remaining_seconds": 0,
                "message": "Trial expired - payment required to continue"
            }
        
        remaining_seconds = int((trial_duration - elapsed).total_seconds())
        return {
            "status": "active",
            "remaining_seconds": remaining_seconds,
            "message": f"Trial active - {remaining_seconds} seconds remaining"
        }


def check_trial_middleware():
    """Middleware decorator to check trial status before processing messages"""
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({
                    "error": "Authentication required",
                    "redirect": "/login"
                }), 401
            
            # Check trial status
            is_allowed, remaining_seconds, message = TrialManager.check_trial_status(current_user)
            
            if not is_allowed:
                return jsonify({
                    "error": "Trial expired",
                    "message": "Your 3-minute free trial has expired. Please complete payment to continue chatting with Aria.",
                    "redirect": "/payment/required",
                    "trial_expired": True
                }), 403
            
            # Add trial info to response headers if trial is active
            if remaining_seconds > 0:
                response = f(*args, **kwargs)
                if hasattr(response, 'headers'):
                    response.headers['X-Trial-Remaining'] = str(remaining_seconds)
                return response
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator