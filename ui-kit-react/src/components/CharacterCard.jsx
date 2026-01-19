import React, { memo } from 'react';
import Spinner from './common/Spinner';
import './CharactersUI.css';

const getRoleColor = (role) => {
  switch(role?.toLowerCase()) {
    case 'protagonist': return 'var(--color-primary)';
    case 'antagonist': return 'var(--color-tension-climax)';
    case 'supporting': return 'var(--color-secondary)';
    default: return 'var(--color-text-muted)';
  }
};

const CharacterCard = memo(({ char, onEdit, onDelete, isDeleting }) => {
  return (
    <div className="char-card" style={{borderTop: `4px solid ${getRoleColor(char.role)}`}}>
      <div className="char-card-header">
        <h5>{char.name}</h5>
        <span className="char-role" style={{color: getRoleColor(char.role)}}>{char.role}</span>
      </div>

      <div className="char-attributes">
        {char.archetype && <div className="char-attr"><strong>Archetype:</strong> {char.archetype}</div>}
        {char.motivation && <div className="char-attr"><strong>Want:</strong> {char.motivation}</div>}
        {char.flaw && <div className="char-attr"><strong>Flaw:</strong> {char.flaw}</div>}
      </div>

      {char.bio && <p className="char-bio">{char.bio}</p>}

      <div className="char-actions">
        <button
          className="btn-text"
          onClick={() => onEdit(char)}
          aria-label={`Edit ${char.name}`}
          title={`Edit ${char.name}`}
          disabled={isDeleting}
        >
          Edit
        </button>
        <button
          className="btn-text delete"
          onClick={() => onDelete(char.id)}
          aria-label={isDeleting ? "Deleting..." : `Delete ${char.name}`}
          title={`Delete ${char.name}`}
          style={{ color: '#ef4444' }}
          disabled={isDeleting}
        >
          {isDeleting ? <Spinner size="small" color="danger" /> : "Delete"}
        </button>
      </div>
    </div>
  );
});

export default CharacterCard;
