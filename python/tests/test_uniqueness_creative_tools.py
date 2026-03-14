import pytest
import re
import asyncio
from python.uniqueness.rituals.oblique_strategy import ObliqueStrategyRitual
from python.uniqueness.traits.sensory_overload import SensoryOverloadTrait

def test_oblique_strategy_ritual():
    ritual = ObliqueStrategyRitual({"enabled": True})

    context_building = {"user_input": "I am stuck on this chapter.", "intent": "building"}

    response = "This is a great scene."
    new_response = asyncio.run(ritual.apply(response))

    assert "Oblique Strategy" in new_response
    assert "<margin-note>" in new_response

    newer_response = asyncio.run(ritual.apply(new_response))
    assert newer_response.count("Oblique Strategy") == 1

def test_sensory_overload_trait():
    trait = SensoryOverloadTrait({"strength": 1.0, "enabled": True})

    context_technical = {"intent": "debugging"}
    resp = "The room is very dark."
    assert asyncio.run(trait.apply(context_technical, resp)) == resp

    context_general = {"intent": "building"}

    resp_room = "The room is empty."
    new_resp = asyncio.run(trait.apply(context_general, resp_room))
    assert new_resp != resp_room
    assert "The room" not in new_resp

    resp_quiet = "It was quiet."
    new_resp2 = asyncio.run(trait.apply(context_general, resp_quiet))
    assert new_resp2 != resp_quiet
