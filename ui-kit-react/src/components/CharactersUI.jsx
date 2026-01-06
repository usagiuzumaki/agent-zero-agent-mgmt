import React, { useState, useEffect } from 'react';
import Spinner from './common/Spinner';
import './CharactersUI.css';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [newChar, setNewChar] = useState({
    name: '',
    role: 'Protagonist',
    archetype: '',
    motivation: '',
    flaw: '',
    bio: ''
  });

  useEffect(() => {
    fetchCharacters();
  }, []);

  const fetchCharacters = async () => {
    try {
      // Using get_all_data for now as there isn't a dedicated list endpoint documented
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

  const resetForm = () => {
    setShowForm(false);
    setEditingId(null);
    setNewChar({ name: '', role: 'Protagonist', archetype: '', motivation: '', flaw: '', bio: '' });
  };

  const handleEdit = (char) => {
    setNewChar({ ...char });
    setEditingId(char.id);
    setShowForm(true);
    // Scroll to top of form area
    const formElement = document.querySelector('.char-form-card');
    if (formElement) formElement.scrollIntoView({ behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this character?")) return;

    try {
      const response = await fetch('/api/screenwriting/character/delete', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      });

      if (response.ok) {
        fetchCharacters();
      }
    } catch (err) {
      console.error("Failed to delete character", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);

    const endpoint = editingId
      ? '/api/screenwriting/character/update'
      : '/api/screenwriting/character/add';

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newChar)
      });

      if (response.ok) {
        resetForm();
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
      case 'protagonist': return 'var(--color-primary)';
      case 'antagonist': return '#ef4444';
      case 'supporting': return '#10b981';
      default: return '#6b7280';
    }
  };

  if (loading) return (
    <div className="loading">
      <Spinner size="md" />
      <span>Loading Cast...</span>
    </div>
  );

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        <button
          className="btn-primary"
          onClick={() => {
            if (showForm) resetForm();
            else setShowForm(true);
          }}
        >
          {showForm ? 'Cancel' : '+ Add Character'}
        </button>
      </div>

      {showForm && (
        <div className="char-form-card">
          <h4>{editingId ? 'Edit Character' : 'New Character Profile'}</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="char-name">Name</label>
                <input
                  id="char-name"
                  value={newChar.name}
                  onChange={e => setNewChar({...newChar, name: e.target.value})}
                  required
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
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', opacity: isSaving ? 0.7 : 1 }}
            >
              {isSaving && <Spinner size="sm" />}
              {isSaving ? 'Saving...' : (editingId ? 'Update Character' : 'Save Character')}
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
                  className="btn-icon"
                  onClick={() => handleEdit(char)}
                  aria-label={`Edit ${char.name}`}
                  title="Edit"
                >
                  ✎
                </button>
                <button
                  className="btn-icon"
                  onClick={() => handleDelete(char.id)}
                  aria-label={`Delete ${char.name}`}
                  title="Delete"
                  style={{color: '#ef4444'}}
                >
                  🗑
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
