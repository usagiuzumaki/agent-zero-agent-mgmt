/**
 * Simple modal wrapper used by the AgentLauncher.
 */
export default function AgentModal({ open, onClose, children }) {
  if (!open) return null;
  return (
    <div className="agent-modal-overlay">
      <div className="agent-modal">
        <button className="close" onClick={onClose} aria-label="Close">
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
