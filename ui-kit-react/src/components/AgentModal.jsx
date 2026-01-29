import { useEffect } from 'react';

/**
 * Simple modal wrapper used by the AgentLauncher.
 */
export default function AgentModal({ open, onClose, children, className = '' }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && open) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  return (
    <div
      className={`agent-modal-overlay ${open ? 'open' : ''}`}
      aria-hidden={!open}
      onClick={onClose}
    >
      <div
        className={`agent-modal ${className}`}
        onClick={(e) => e.stopPropagation()}
      >
        <button className="close" onClick={onClose} aria-label="Close">
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
