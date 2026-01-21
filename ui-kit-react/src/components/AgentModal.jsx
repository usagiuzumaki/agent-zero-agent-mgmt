/**
 * Simple modal wrapper used by the AgentLauncher.
 */
export default function AgentModal({ open, onClose, children }) {
  return (
    <div className={`agent-modal-overlay ${open ? 'open' : ''}`} aria-hidden={!open}>
      <div className="agent-modal">
        <button className="close" onClick={onClose} aria-label="Close">
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
