/**
 * Floating button that opens the agent UI.
 */
export default function AgentLauncher({ onOpen }) {
  return (
    <button className="agent-launcher" onClick={onOpen}>
      Open Agent
    </button>
  );
}
