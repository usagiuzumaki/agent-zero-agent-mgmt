import React, { useState, useEffect, useCallback } from 'react';
import Spinner from './common/Spinner';
import CharacterCard from './CharacterCard';
import './CharactersUI.css';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  const [newChar, setNewChar] = useState({
    name: '',
    role: 'Protagonist',
    archetype: '',
    motivation: '',
    flaw: '',
    bio: ''
  });

  const fetchCharacters = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    fetchCharacters();
  }, [fetchCharacters]);

  const handleEdit = useCallback((char) => {
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
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleCancel = useCallback(() => {
    setShowForm(false);
    setEditingId(null);
    setNewChar({
      name: '',
      role: 'Protagonist',
      archetype: '',
      motivation: '',
      flaw: '',
      bio: ''
    });
  }, []);

  const handleDelete = useCallback(async (charId) => {
    if (!window.confirm("Are you sure you want to delete this character?")) return;

    setDeletingId(charId);
    try {
      const response = await fetch('/api/screenwriting/character/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: charId })
      });

      if (response.ok) {
        fetchCharacters();
        // If we were editing this character, reset form
        if (editingId === charId) {
          handleCancel();
        }
      }
    } catch (err) {
      console.error("Failed to delete character", err);
    } finally {
      setDeletingId(null);
    }
  }, [editingId, fetchCharacters, handleCancel]);

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

  if (loading) return (
    <div className="loading-container">
      <Spinner size="lg" color="primary" />
      <p>Loading Cast...</p>
    </div>
  );

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        <button
          className={showForm ? "btn-secondary" : "btn-primary"}
          onClick={showForm ? handleCancel : () => setShowForm(true)}
          aria-expanded={showForm}
          aria-controls="char-form"
        >
          {showForm ? 'Cancel' : '+ Add Character'}
        </button>
      </div>

      {showForm && (
        <div id="char-form" className="char-form-card">
          <h4>{editingId ? 'Edit Character Profile' : 'New Character Profile'}</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="char-name">
                  Name <span className="required-star" aria-hidden="true">*</span>
                </label>
                <input
                  id="char-name"
                  value={newChar.name}
                  onChange={e => setNewChar({...newChar, name: e.target.value})}
                  required
                  aria-required="true"
                  placeholder="Character Name"
                  autoFocus
                />
              </div>
              <div className="form-group">
                <label htmlFor="char-role">Role</label>
                <select
                  id="char-role"
                  value={newChar.role}
                  onChange={e => setNewChar({...newChar, role: e.target.value})}
                >
                  <option>Protagonist</option>
                  <option>Antagonist</option>
                  <option>Supporting</option>
                  <option>Minor</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="char-archetype">Archetype</label>
                <input
                  id="char-archetype"
                  placeholder="e.g. The Reluctant Hero"
                  value={newChar.archetype}
                  onChange={e => setNewChar({...newChar, archetype: e.target.value})}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="char-motivation">Motivation (Want)</label>
                <input
                  id="char-motivation"
                  value={newChar.motivation}
                  onChange={e => setNewChar({...newChar, motivation: e.target.value})}
                  placeholder="What drives them?"
                />
              </div>
              <div className="form-group">
                <label htmlFor="char-flaw">Fatal Flaw (Need)</label>
                <input
                  id="char-flaw"
                  value={newChar.flaw}
                  onChange={e => setNewChar({...newChar, flaw: e.target.value})}
                  placeholder="What holds them back?"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="char-bio">Bio & Notes</label>
              <textarea
                id="char-bio"
                rows={3}
                value={newChar.bio}
                onChange={e => setNewChar({...newChar, bio: e.target.value})}
                placeholder="Backstory, physical description, or key traits..."
              />
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={handleCancel}
                style={{ marginRight: '1rem' }}
              >
                Cancel
              </button>
              <button type="submit" className="btn-save" disabled={isSaving} style={{ marginTop: 0 }}>
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
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="empty-state-icon" aria-hidden="true">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <p className="empty-state-text">
              No characters yet. Every story needs a cast! Create your first character to begin building your ensemble.
            </p>
            <button
              className="btn-primary"
              onClick={() => setShowForm(true)}
            >
              Create First Character
            </button>
          </div>
        ) : (
          characters.map((char) => (
            <CharacterCard
              key={char.id}
              char={char}
              onEdit={handleEdit}
              onDelete={handleDelete}
              isDeleting={deletingId === char.id}
            />
          ))
        )}
      </div>
    </div>
  );
}
