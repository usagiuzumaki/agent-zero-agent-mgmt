/**
 * Displays agent logs for debugging/audit purposes.
 */
export default function AgentLogView({ logs }) {
  return (
    <div className="agent-log">
      {logs.map((log, idx) => (
        <pre key={idx}>{log}</pre>
      ))}
    </div>
  );
}
