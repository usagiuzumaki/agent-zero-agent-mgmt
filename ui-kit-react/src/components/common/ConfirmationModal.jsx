import React, { useEffect, useRef } from 'react';
import './ConfirmationModal.css';

export default function ConfirmationModal({
  isOpen,
  title,
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
  isProcessing = false
}) {
  const modalRef = useRef(null);
  const confirmBtnRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Focus the confirmation button when modal opens for safety/convenience
      // Or maybe the cancel button to prevent accidental clicks?
      // Let's focus the Cancel button for safety.
      // Actually, standard pattern often focuses the first interactive element or the modal itself.
      // Let's focus the modal container.
      if (modalRef.current) {
        modalRef.current.focus();
      }
    }
  }, [isOpen]);

  // Trap focus (simple implementation)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;
      if (e.key === 'Escape') {
        onCancel();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="modal-content" ref={modalRef} tabIndex={-1}>
        <h3 id="modal-title">{title}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          <button
            className="btn-secondary"
            onClick={onCancel}
            disabled={isProcessing}
          >
            {cancelLabel}
          </button>
          <button
            ref={confirmBtnRef}
            className="btn-danger"
            onClick={onConfirm}
            disabled={isProcessing}
          >
            {isProcessing ? 'Processing...' : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
