from agents import AgentContext, UserMessage
from python.helpers.api import ApiHandler, Request, Response

from python.helpers import files
import os
from werkzeug.utils import secure_filename
from python.helpers.defer import DeferredTask
from python.helpers.print_style import PrintStyle

# Import trial management
try:
    from flask_login import current_user
    from trial_manager import TrialManager
    from flask import jsonify
    _trial_management_available = True
except ImportError:
    _trial_management_available = False
    PrintStyle().print("Warning: Trial management not available")


class Message(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        result = await self.communicate(input=input, request=request)
        
        # Check if this is a trial error response
        if isinstance(result, tuple) and result[0] is None:
            return result[1]  # Return the error response directly
        
        task, context = result
        return await self.respond(task, context)

    async def respond(self, task: DeferredTask, context: AgentContext):
        result = await task.result()  # type: ignore
        return {
            "message": result,
            "context": context.id,
        }

    async def communicate(self, input: dict, request: Request):
        # Check trial status if trial management is available
        if _trial_management_available:
            try:
                # In Flask, current_user is a proxy that needs to be accessed in request context
                from flask import has_request_context
                if has_request_context() and current_user.is_authenticated:
                    # Check trial status
                    is_allowed, remaining_seconds, message = TrialManager.check_trial_status(current_user)
                    
                    if not is_allowed:
                        # Trial expired, return error response
                        return None, {
                            "error": "Trial expired",
                            "message": "Your 3-minute free trial has expired. Please complete payment to continue chatting with Aria.",
                            "redirect": "/payment/required",
                            "trial_expired": True,
                            "remaining_seconds": 0
                        }
            except Exception as e:
                PrintStyle().print(f"Trial check error: {e}")
                # Continue without trial check if there's an error
        
        # Handle both JSON and multipart/form-data
        if request.content_type.startswith("multipart/form-data"):
            text = request.form.get("text", "")
            ctxid = request.form.get("context", "")
            message_id = request.form.get("message_id", None)
            attachments = request.files.getlist("attachments")
            attachment_paths = []

            upload_folder_int = "/a0/tmp/uploads"
            upload_folder_ext = files.get_abs_path("tmp/uploads") # for development environment

            if attachments:
                os.makedirs(upload_folder_ext, exist_ok=True)
                for attachment in attachments:
                    if attachment.filename is None:
                        continue
                    filename = secure_filename(attachment.filename)
                    save_path = files.get_abs_path(upload_folder_ext, filename)
                    attachment.save(save_path)
                    attachment_paths.append(os.path.join(upload_folder_int, filename))
        else:
            # Handle JSON request as before
            input_data = request.get_json()
            text = input_data.get("text", "")
            ctxid = input_data.get("context", "")
            message_id = input_data.get("message_id", None)
            attachment_paths = []

        # Now process the message
        message = text

        # Obtain agent context
        context = self.get_context(ctxid)

        # Store attachments in agent data
        # context.agent0.set_data("attachments", attachment_paths)

        # Prepare attachment filenames for logging
        attachment_filenames = (
            [os.path.basename(path) for path in attachment_paths]
            if attachment_paths
            else []
        )

        # Print to console and log
        PrintStyle(
            background_color="#6C3483", font_color="white", bold=True, padding=True
        ).print(f"User message:")
        PrintStyle(font_color="white", padding=False).print(f"> {message}")
        if attachment_filenames:
            PrintStyle(font_color="white", padding=False).print("Attachments:")
            for filename in attachment_filenames:
                PrintStyle(font_color="white", padding=False).print(f"- {filename}")

        # Log the message with message_id and attachments
        context.log.log(
            type="user",
            heading="User message",
            content=message,
            kvps={"attachments": attachment_filenames},
            id=message_id,
        )

        return context.communicate(UserMessage(message, attachment_paths)), context
