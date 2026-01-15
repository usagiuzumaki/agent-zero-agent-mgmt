const tools = [];

/** Register a custom tool that can be invoked from the AgentChat. */
export function registerTool(tool) {
  tools.push(tool);
}

/** Get all registered tools. */
export function getTools() {
  return tools;
}

// --- Default Tools ---

registerTool({
  name: 'reset-chat',
  label: 'Reset Chat',
  action: async (callback) => {
    try {
      const res = await fetch('/api/chat/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: 'default' }) // Assuming default context
      });
      if (res.ok) {
        callback('Chat has been reset.');
        // Optionally trigger a page reload or state clear if the UI needs it
        // but callback just adds a message.
        // For a true reset, we might want to clear the local messages state too?
        // But the `action` callback is limited to adding a message.
        // We might need a more powerful tool interface later.
        window.location.reload();
      } else {
        callback('Failed to reset chat.');
      }
    } catch (e) {
      callback(`Error: ${e.message}`);
    }
  }
});

registerTool({
  name: 'restart-agent',
  label: 'Restart Agent',
  action: async (callback) => {
    try {
      const res = await fetch('/api/restart', { method: 'POST' });
      if (res.ok) {
        callback('Agent system is restarting...');
        setTimeout(() => window.location.reload(), 2000);
      } else {
        callback('Failed to restart agent.');
      }
    } catch (e) {
      callback(`Error: ${e.message}`);
    }
  }
});

registerTool({
  name: 'clear-log',
  label: 'Clear Log',
  action: (callback) => {
    // This is a bit hacky as we don't have access to the setLogs from here easily without a better context.
    // But we can just say "Logs cleared" for now or use a global event.
    console.clear();
    callback('Console logs cleared.');
  }
});
