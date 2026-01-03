import React from 'react';
import './Spinner.css';

export default function Spinner({ size = 'medium', color = 'var(--color-primary)' }) {
  return (
    <div
      className={`spinner spinner-${size}`}
      style={{ borderTopColor: color }}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
