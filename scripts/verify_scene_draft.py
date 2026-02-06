import sys
import os
import json
import asyncio

# Add root directory to path
sys.path.append(os.getcwd())

# Mock necessary modules before importing run_ui to avoid side effects
from unittest.mock import MagicMock

from run_ui import webapp
from python.api.screenwriting import screenwriting_bp
webapp.register_blueprint(screenwriting_bp)

def test_draft_scene():
    client = webapp.test_client()

    # Mock data
    payload = {
        "beat_summary": "A tense standoff between the hero and the villain on a rooftop in the rain.",
        "scene_title": "The Final Confrontation"
    }

    from unittest.mock import patch

    # Patch the draft method to return a dummy script immediately
    with patch('agents.screenwriting.co_writer.CoWriter.draft', new_callable=MagicMock) as mock_draft:
        # Since draft is awaited, the mock needs to be awaitable if it were a real async function,
        # but the route calls `await agent.draft(prompt)`.
        # MagicMock return_value is not awaitable by default unless we set it up.

        # Helper to create awaitable result
        f = asyncio.Future()
        f.set_result("INT. ROOFTOP - NIGHT\n\nRain pours down...\n\nHERO\nIt ends here.")
        mock_draft.return_value = f

        response = client.post('/api/screenwriting/scene/draft',
                               data=json.dumps(payload),
                               content_type='application/json')

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json}")

        if response.status_code != 200:
             print("Registered Routes:")
             print(webapp.url_map)

        assert response.status_code == 200
        assert "INT. ROOFTOP" in response.json['result']

if __name__ == "__main__":
    try:
        test_draft_scene()
        print("✅ Verification passed!")
    except AssertionError as e:
        print(f"❌ Verification failed: Assertion Error")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
