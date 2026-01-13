import React, { memo } from 'react';
import './CharactersUI.css';

const CharacterCard = memo(({ char, onEdit, onDelete }) => {
  const getRoleColor = (role) => {
    switch(role?.toLowerCase()) {
      case 'protagonist': return 'var(--color-primary)';
      case 'antagonist': return 'var(--color-tension-climax)';
      case 'supporting': return 'var(--color-secondary)';
      default: return 'var(--color-text-muted)';
    }
  };

  const roleColor = getRoleColor(char.role);

  return (
    <div className="char-card" style={{borderTop: `4px solid ${roleColor}`}}>
      <div className="char-card-header">
        <h5>{char.name}</h5>
        <span className="char-role" style={{color: roleColor}}>{char.role}</span>
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
        >
          Edit
        </button>
        <button
          className="btn-text delete"
          onClick={() => onDelete(char.id)}
          aria-label={`Delete ${char.name}`}
          style={{ color: '#ef4444' }}
        >
          Delete
        </button>
      </div>
    </div>
  );
});

CharacterCard.displayName = 'CharacterCard';

export default CharacterCard;
