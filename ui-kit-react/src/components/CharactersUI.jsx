import React, { useState, useEffect } from 'react';
import Spinner from './common/Spinner';
import './CharactersUI.css';
import Spinner from './common/Spinner';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);

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
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (charId) => {
    if (!window.confirm("Are you sure you want to delete this character?")) return;

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
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setNewChar(initialCharState);
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
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this character?')) return;

    try {
      const response = await fetch('/api/screenwriting/character/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      });

      if (response.ok) {
        fetchCharacters();
      }
    } catch (err) {
      console.error("Failed to add character", err);
    } finally {
      setIsSaving(false);
    }
  };

  const getRoleColor = (role) => {
    switch(role.toLowerCase()) {
      case 'protagonist': return 'var(--color-primary)';
      case 'antagonist': return '#ef4444';
      case 'supporting': return '#10b981';
      default: return '#6b7280';
    }
  };

  if (loading) return (
    <div className="loading-container">
      <Spinner size="lg" color="var(--color-primary)" />
      <p>Loading Cast...</p>
    </div>
  );

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        <button
          className="btn-primary"
          onClick={() => setShowForm(!showForm)}
          aria-expanded={showForm}
          aria-controls="char-form"
        >
          {showForm ? 'Cancel' : '+ Add Character'}
        </button>
      </div>

      {showForm && (
        <div id="char-form" className="char-form-card">
          <h4>New Character Profile</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="char-name">Name</label>
                <input
                  id="char-name"
                  value={newChar.name}
                  onChange={e => setNewChar({...newChar, name: e.target.value})}
                  required
                  aria-required="true"
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
                />
              </div>
              <div className="form-group">
                <label htmlFor="char-flaw">Fatal Flaw (Need)</label>
                <input
                  id="char-flaw"
                  value={newChar.flaw}
                  onChange={e => setNewChar({...newChar, flaw: e.target.value})}
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
              />
            </div>

            <button
              type="submit"
              className="btn-save"
              disabled={isSaving}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'center' }}
            >
              {isSaving ? <Spinner size="sm" color="white" /> : null}
              {isSaving ? 'Saving...' : 'Save Character'}
            </button>
          </form>
        </div>
      )}

      <div className="chars-grid">
        {characters.length === 0 ? (
          <p className="empty-state">No characters yet. Start building your cast!</p>
        ) : (
          characters.map((char) => (
            <div key={char.id} className="char-card" style={{borderTop: `4px solid ${getRoleColor(char.role)}`}}>
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
                  onClick={() => handleEdit(char)}
                  aria-label={`Edit ${char.name}`}
                >
                  Edit
                </button>
                <button
                  className="btn-text delete"
                  onClick={() => handleDelete(char.id)}
                  aria-label={`Delete ${char.name}`}
                  style={{ color: '#ef4444' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
