import AgentChat from './AgentChat';

export default function ScreenwritingUI({ onLog }) {
  return (
    <div className="screenwriting-ui">
      <h2>Screenwriting Assistant</h2>
      <AgentChat onLog={onLog} />
    </div>
  );
}
