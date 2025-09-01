import AgentChat from './AgentChat';

export default function EgirlUI({ onLog }) {
  return (
    <div className="egirl-ui">
      <h2>E-Girl Companion</h2>
      <AgentChat onLog={onLog} />
    </div>
  );
}
