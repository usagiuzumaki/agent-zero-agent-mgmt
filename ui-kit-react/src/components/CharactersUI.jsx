import React, { useState, useEffect, useRef } from 'react';
import Spinner from './common/Spinner';
import ConfirmationModal from './common/ConfirmationModal';
import './CharactersUI.css';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [charToDelete, setCharToDelete] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const nameInputRef = useRef(null);

  const initialCharState = {
    name: '',
    role: 'Protagonist',
    archetype: '',
    motivation: '',
    flaw: '',
    bio: ''
  };

  const [newChar, setNewChar] = useState(initialCharState);

  useEffect(() => {
    fetchCharacters();
  }, []);

  // Focus management
  useEffect(() => {
    if (showForm && nameInputRef.current) {
      nameInputRef.current.focus();
    }
  }, [showForm]);

  const fetchCharacters = async () => {
    try {
      const response = await fetch('/api/screenwriting/all');
      const data = await response.json();
      if (data.character_profiles && data.character_profiles.characters) {
        setCharacters(data.character_profiles.characters);
      }
    } catch (err) {
      console.error("Failed to load characters", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (char) => {
    setNewChar({
      name: char.name || '',
      role: char.role || 'Protagonist',
      archetype: char.archetype || '',
      motivation: char.motivation || '',
      flaw: char.flaw || '',
      bio: char.bio || ''
    });
    setEditingId(char.id);
    setShowForm(true);
    // Scroll to form
    const formElement = document.getElementById('char-form');
    if (formElement) {
        formElement.scrollIntoView({ behavior: 'smooth' });
    } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setNewChar(initialCharState);
  };

  const confirmDelete = (char) => {
    setCharToDelete(char);
    setDeleteConfirmOpen(true);
  };

  const handleDelete = async () => {
    if (!charToDelete) return;
    setIsDeleting(true);

    try {
      const response = await fetch('/api/screenwriting/character/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: charToDelete.id })
      });

      if (response.ok) {
        fetchCharacters();
        // If we were editing this character, reset form
        if (editingId === charToDelete.id) {
          handleCancel();
        }
      }
    } catch (err) {
      console.error("Failed to delete character", err);
    } finally {
      setIsDeleting(false);
      setDeleteConfirmOpen(false);
      setCharToDelete(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      let response;
      if (editingId) {
        // Update existing character
        response = await fetch('/api/screenwriting/character/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: editingId,
            data: newChar
          })
        });
      } else {
        // Create new character
        response = await fetch('/api/screenwriting/character/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newChar)
        });
      }

      if (response.ok) {
        handleCancel();
        fetchCharacters();
      }
    } catch (err) {
      console.error("Failed to save character", err);
    } finally {
      setIsSaving(false);
    }
  };

  const getRoleColor = (role) => {
    switch(role.toLowerCase()) {
      case 'protagonist': return 'var(--color-primary, #4f46e5)';
      case 'antagonist': return 'var(--color-tension-climax, #ef4444)';
      case 'supporting': return 'var(--color-secondary, #10b981)';
      default: return 'var(--color-text-muted, #6b7280)';
    }
  };

  if (loading) return (
    <div className="loading-container">
      <Spinner size="large" color="primary" />
      <p>Loading Cast...</p>
    </div>
  );

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        {!showForm && (
            <button
            className="btn-primary"
            onClick={() => setShowForm(true)}
            aria-expanded={showForm}
            >
            + Add Character
            </button>
        )}
      </div>

      {showForm && (
        <div id="char-form" className="char-form-card fade-in" role="region" aria-label="Character Form">
          <div className="form-header">
             <h4>{editingId ? 'Edit Character Profile' : 'New Character Profile'}</h4>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group span-2">
                <label htmlFor="char-name">
                  Name <span className="required-star" aria-hidden="true">*</span>
                </label>
                <input
                  id="char-name"
                  ref={nameInputRef}
                  value={newChar.name}
                  onChange={e => setNewChar({...newChar, name: e.target.value})}
                  required
                  aria-required="true"
                  placeholder="Character Name"
                  className="input-field"
                />
              </div>

              <div className="form-group">
                <label htmlFor="char-role">Role</label>
                <select
                  id="char-role"
                  value={newChar.role}
                  onChange={e => setNewChar({...newChar, role: e.target.value})}
                  className="select-field"
                >
                  <option>Protagonist</option>
                  <option>Antagonist</option>
                  <option>Supporting</option>
                  <option>Minor</option>
                </select>
              </div>

               <div className="form-group">
                <label htmlFor="char-archetype">Archetype</label>
                <input
                  id="char-archetype"
                  placeholder="e.g. The Reluctant Hero"
                  value={newChar.archetype}
                  onChange={e => setNewChar({...newChar, archetype: e.target.value})}
                  className="input-field"
                />
              </div>

              <div className="form-group">
                <label htmlFor="char-motivation">Motivation (Want)</label>
                <input
                  id="char-motivation"
                  value={newChar.motivation}
                  onChange={e => setNewChar({...newChar, motivation: e.target.value})}
                  placeholder="What drives them?"
                  className="input-field"
                />
              </div>

              <div className="form-group">
                <label htmlFor="char-flaw">Fatal Flaw (Need)</label>
                <input
                  id="char-flaw"
                  value={newChar.flaw}
                  onChange={e => setNewChar({...newChar, flaw: e.target.value})}
                  placeholder="What holds them back?"
                  className="input-field"
                />
              </div>

              <div className="form-group span-full">
                <label htmlFor="char-bio">Bio & Notes</label>
                <textarea
                  id="char-bio"
                  rows={4}
                  value={newChar.bio}
                  onChange={e => setNewChar({...newChar, bio: e.target.value})}
                  placeholder="Backstory, physical description, or key traits..."
                  className="textarea-field"
                />
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={handleCancel}
                disabled={isSaving}
              >
                Cancel
              </button>
              <button type="submit" className="btn-save" disabled={isSaving}>
                {isSaving ? (
                  <div className="btn-save-content">
                    <Spinner size="small" color="white" />
                    <span>Saving...</span>
                  </div>
                ) : (
                  'Save Character'
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="chars-grid">
        {characters.length === 0 ? (
          <div className="empty-state-container">
            <p className="empty-state-text">
              No characters yet. Every story needs a cast!
            </p>
            {!showForm && (
                <button
                className="btn-primary"
                onClick={() => setShowForm(true)}
                >
                Create First Character
                </button>
            )}
          </div>
        ) : (
          characters.map((char) => (
            <div key={char.id} className="char-card" style={{borderTop: `4px solid ${getRoleColor(char.role)}`}}>
              <div className="char-card-header">
                <h5>{char.name}</h5>
                <span className="char-role-badge" style={{backgroundColor: getRoleColor(char.role) + '20', color: getRoleColor(char.role)}}>
                    {char.role}
                </span>
              </div>

              <div className="char-attributes">
                {char.archetype && <div className="char-attr"><span className="attr-label">Archetype:</span> {char.archetype}</div>}
                {char.motivation && <div className="char-attr"><span className="attr-label">Want:</span> {char.motivation}</div>}
                {char.flaw && <div className="char-attr"><span className="attr-label">Flaw:</span> {char.flaw}</div>}
              </div>

              {char.bio && <p className="char-bio">{char.bio}</p>}

              <div className="char-actions">
                <button
                  className="btn-text"
                  onClick={() => handleEdit(char)}
                  aria-label={`Edit ${char.name}`}
                >
                  Edit
                </button>
                <button
                  className="btn-text delete"
                  onClick={() => confirmDelete(char)}
                  aria-label={`Delete ${char.name}`}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <ConfirmationModal
        isOpen={deleteConfirmOpen}
        title="Delete Character"
        message={`Are you sure you want to delete ${charToDelete?.name}? This action cannot be undone.`}
        confirmLabel="Delete"
        cancelLabel="Keep"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirmOpen(false)}
        isProcessing={isDeleting}
      />
    </div>
  );
}
