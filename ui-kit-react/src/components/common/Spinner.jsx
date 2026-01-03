import React from 'react';
import './Spinner.css';

export default function Spinner({ size = '1em', color = 'currentColor' }) {
  return (
    <div
      className="spinner"
      role="status"
      style={{
        width: size,
        height: size,
        borderColor: `${color} transparent ${color} transparent`
      }}
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
