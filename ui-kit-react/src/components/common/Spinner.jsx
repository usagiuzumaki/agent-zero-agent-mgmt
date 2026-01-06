import React from 'react';
import './Spinner.css';

/**
 * Reusable Spinner Component
 * @param {Object} props
 * @param {'sm' | 'md' | 'lg'} [props.size='sm'] - Size of the spinner
 * @param {string} [props.color='currentColor'] - Color of the spinner
 * @param {string} [props.className=''] - Additional class names
 */
const Spinner = ({ size = 'sm', color = 'currentColor', className = '' }) => {
  return (
    <div
      className={`spinner spinner-${size} ${className}`}
      style={{ borderTopColor: color }}
      role="status"
      aria-label="Loading"
    />
  );
};

export default Spinner;
