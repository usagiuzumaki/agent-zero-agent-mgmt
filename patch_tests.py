import re
with open('python/tests/test_uniqueness_creative_tools.py', 'r') as f:
    content = f.read()

# Make tests sync to avoid pytest-asyncio issues in this sandbox
content = content.replace("async def test_oblique_strategy_ritual", "def test_oblique_strategy_ritual")
content = content.replace("await ritual.apply", "__import__('asyncio').run(ritual.apply")
content = content.replace("new_response)", "new_response))")
content = content.replace("response)", "response))")

content = content.replace("async def test_sensory_overload_trait", "def test_sensory_overload_trait")
content = content.replace("await trait.apply", "__import__('asyncio').run(trait.apply")
content = content.replace("resp)", "resp))")
content = content.replace("resp_room)", "resp_room))")
content = content.replace("resp_quiet)", "resp_quiet))")
content = content.replace("@pytest.mark.asyncio\n", "")

with open('python/tests/test_uniqueness_creative_tools.py', 'w') as f:
    f.write(content)
