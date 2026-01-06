import React from 'react';
import './Spinner.css';

export default function Spinner({ size = 'sm', color = 'currentColor' }) {
  const dims = {
    sm: '16px',
    md: '24px',
    lg: '32px'
  };

  return (
    <div
      className="spinner"
      role="status"
      aria-label="Loading"
      style={{
        width: dims[size],
        height: dims[size],
        border: `2px solid ${color}`,
        borderRightColor: 'transparent'
      }}
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
