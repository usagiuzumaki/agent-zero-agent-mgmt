import React from 'react';
import './Spinner.css';

export default function Spinner({ size = 'medium', color = 'primary' }) {
  return <div className={`spinner spinner-${size} spinner-${color}`} aria-label="Loading" role="status" />;
}
