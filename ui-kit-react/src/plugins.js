const tools = [];

/** Register a custom tool that can be invoked from the AgentChat. */
export function registerTool(tool) {
  tools.push(tool);
}

/** Get all registered tools. */
export function getTools() {
  return tools;
}
