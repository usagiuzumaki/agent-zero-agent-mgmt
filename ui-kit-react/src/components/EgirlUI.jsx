import AgentChat from './AgentChat';

export default function EgirlUI({ onLog }) {
  return (
    <div className="egirl-ui">
      <div className="aria-container">
        <div className="aria-header">
          <h2>Aria - Your Creative Companion</h2>
          <div className="status-indicator">Creative Mode Active</div>
        </div>
        <AgentChat onLog={onLog} />
      </div>
    </div>
  );
}
