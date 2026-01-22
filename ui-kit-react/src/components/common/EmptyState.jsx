import React from 'react';
import './EmptyState.css';

export default function EmptyState({ icon, title, description, action }) {
  return (
    <div className="empty-state-container">
      {icon && <div aria-hidden="true">{icon}</div>}
      {title && <h4 className="empty-state-title">{title}</h4>}
      {description && <p className="empty-state-text">{description}</p>}
      {action && <div className="empty-state-action">{action}</div>}
    </div>
  );
}
