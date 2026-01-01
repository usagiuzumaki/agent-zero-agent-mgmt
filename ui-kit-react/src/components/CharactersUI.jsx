import React, { useState, useEffect } from 'react';
import './CharactersUI.css';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/screenwriting/character/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newChar)
      });

      if (response.ok) {
        setShowForm(false);
        setNewChar({ name: '', role: 'Protagonist', archetype: '', motivation: '', flaw: '', bio: '' });
        fetchCharacters();
      }
    } catch (err) {
      console.error("Failed to add character", err);
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

  if (loading) return <div className="loading">Loading Cast...</div>;

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Character'}
        </button>
      </div>

      {showForm && (
        <div className="char-form-card">
          <h4>New Character Profile</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Name</label>
                <input
                  value={newChar.name}
                  onChange={e => setNewChar({...newChar, name: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Role</label>
                <select
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
                <label>Archetype</label>
                <input
                  placeholder="e.g. The Reluctant Hero"
                  value={newChar.archetype}
                  onChange={e => setNewChar({...newChar, archetype: e.target.value})}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Motivation (Want)</label>
                <input
                  value={newChar.motivation}
                  onChange={e => setNewChar({...newChar, motivation: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Fatal Flaw (Need)</label>
                <input
                  value={newChar.flaw}
                  onChange={e => setNewChar({...newChar, flaw: e.target.value})}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Bio & Notes</label>
              <textarea
                rows={3}
                value={newChar.bio}
                onChange={e => setNewChar({...newChar, bio: e.target.value})}
              />
            </div>

            <button type="submit" className="btn-save">Save Character</button>
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
            </div>
          ))
        )}
      </div>
    </div>
  );
}
