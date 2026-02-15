import React, { memo } from 'react';
import Spinner from './common/Spinner';
import './CharactersUI.css';

const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
};

const getRoleColor = (role) => {
  switch(role?.toLowerCase()) {
    case 'protagonist': return '#6366f1'; // Indigo
    case 'antagonist': return '#ef4444'; // Red
    case 'supporting': return '#10b981'; // Emerald
    default: return '#a3a3a3';
  }
};

const CharacterCard = memo(({ char, onEdit, onDelete, isDeleting }) => {
  const roleColor = getRoleColor(char.role);

  return (
    <div className="char-card" style={{borderTopColor: roleColor}}>
      <div className="char-card-header">
        <div className="char-avatar" style={{background: `linear-gradient(135deg, ${roleColor}, #262626)`}}>
            {getInitials(char.name)}
        </div>
        <div className="char-info">
            <h5>{char.name}</h5>
            <span className="char-role-badge" style={{color: roleColor, borderColor: roleColor, border: '1px solid'}}>
                {char.role}
            </span>
        </div>
      </div>

      <div className="char-attributes">
        {char.archetype && (
            <div className="char-attr-row">
                <span className="attr-label">Archetype</span>
                <span className="attr-value">{char.archetype}</span>
            </div>
        )}
        {char.motivation && (
             <div className="char-attr-row">
                <span className="attr-label">Want</span>
                <span className="attr-value">{char.motivation}</span>
            </div>
        )}
      </div>

      {char.bio && <p className="char-bio">{char.bio}</p>}

      <div className="char-actions">
        <button
          className="btn-studio-secondary"
          onClick={() => onEdit(char)}
          disabled={isDeleting}
          style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem'}}
        >
          Edit
        </button>
        <button
          className="btn-studio-secondary"
          onClick={() => onDelete(char.id)}
          disabled={isDeleting}
          style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', color: '#ef4444', borderColor: '#ef4444'}}
        >
          {isDeleting ? <Spinner size="small" /> : 'Delete'}
        </button>
      </div>
    </div>
  );
});

export default CharacterCard;
