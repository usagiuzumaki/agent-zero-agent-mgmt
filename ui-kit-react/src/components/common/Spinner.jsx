import React from 'react';

export default function Spinner({ size = 'sm', color = 'currentColor' }) {
  const sizeMap = {
    sm: '1rem',
    md: '1.5rem',
    lg: '2.5rem'
  };

  const width = sizeMap[size] || sizeMap.sm;

  return (
    <svg
      className="spinner"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        width: width,
        height: width,
        animation: 'spin 1s linear infinite'
      }}
      role="status"
      aria-label="Loading"
    >
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke={color}
        strokeWidth="4"
        style={{ opacity: 0.25 }}
      />
      <path
        className="opacity-75"
        fill={color}
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        style={{ opacity: 0.75 }}
      />
    </svg>
  );
}
