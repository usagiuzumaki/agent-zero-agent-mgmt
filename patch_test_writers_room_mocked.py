import re
with open('python/tests/test_writers_room_mocked.py', 'r') as f:
    content = f.read()

content = content.replace("@pytest.mark.asyncio\nasync def test_tool_generate_plot_twist():", "def test_tool_generate_plot_twist():")
content = content.replace("response = await tool.execute()", "response = __import__('asyncio').run(tool.execute())")
content = content.replace("@pytest.mark.asyncio\nasync def test_tool_rewrite_from_perspective():", "def test_tool_rewrite_from_perspective():")

with open('python/tests/test_writers_room_mocked.py', 'w') as f:
    f.write(content)
