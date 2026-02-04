/**
 * Simple modal wrapper used by the AgentLauncher.
 */
import { useEffect } from 'react';

export default function AgentModal({ open, onClose, children, className = '' }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (open && e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  return (
    <div
      className={`agent-modal-overlay ${open ? 'open' : ''}`}
      aria-hidden={!open}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className={`agent-modal ${className}`}>
        <button className="close" onClick={onClose} aria-label="Close">
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
