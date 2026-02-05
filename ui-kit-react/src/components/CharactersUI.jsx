import React, { useState, useEffect, useCallback } from 'react';
import Spinner from './common/Spinner';
import EmptyState from './common/EmptyState';
import CharacterCard from './CharacterCard';
import './CharactersUI.css';

export default function CharactersUI() {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showDrawer, setShowDrawer] = useState(false);
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
    setShowDrawer(true);
  }, []);

  const handleCancel = useCallback(() => {
    setShowDrawer(false);
    setTimeout(() => {
        setEditingId(null);
        setNewChar({
          name: '',
          role: 'Protagonist',
          archetype: '',
          motivation: '',
          flaw: '',
          bio: ''
        });
    }, 300); // Wait for transition
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
        response = await fetch('/api/screenwriting/character/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: editingId,
            data: newChar
          })
        });
      } else {
        response = await fetch('/api/screenwriting/character/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newChar)
        });
      }

      if (response.ok) {
        setShowDrawer(false);
        fetchCharacters();
        handleCancel(); // Reset form
      }
    } catch (err) {
      console.error("Failed to save character", err);
    } finally {
      setIsSaving(false);
    }
  };

  const handleGenerate = () => {
     // Mock generation
     setNewChar(prev => ({
         ...prev,
         archetype: prev.archetype || 'The Reluctant Hero',
         motivation: prev.motivation || 'To save their family from impending doom.',
         flaw: prev.flaw || 'Cannot trust anyone.'
     }));
  };

  if (loading) return (
    <div className="loading-container" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%'}}>
      <Spinner size="large" color="primary" />
    </div>
  );

  return (
    <div className="characters-ui">
      <div className="chars-header">
        <h3>Cast of Characters</h3>
        <button
          className="btn-studio-primary"
          onClick={() => setShowDrawer(true)}
        >
          + Add Character
        </button>
      </div>

      <div className="chars-grid">
        {characters.length === 0 ? (
          <EmptyState
            icon={<span>👥</span>}
            title="No Characters Found"
            description="Every story needs a cast! Start by creating your first character."
            action={
              <button
                className="btn-studio-primary"
                onClick={() => setShowDrawer(true)}
              >
                Create First Character
              </button>
            }
          />
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

      {/* Side Drawer */}
      <div className={`char-drawer-overlay ${showDrawer ? 'open' : ''}`} onClick={(e) => {
          if(e.target === e.currentTarget) handleCancel();
      }}>
        <div className="char-drawer">
            <div className="drawer-header">
                <h4>{editingId ? 'Edit Profile' : 'New Character'}</h4>
            </div>

            <form onSubmit={handleSubmit} className="drawer-form">
                <div className="form-group">
                    <label htmlFor="char-name">Name</label>
                    <input
                        id="char-name"
                        value={newChar.name}
                        onChange={e => setNewChar({...newChar, name: e.target.value})}
                        required
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

                <div className="form-group">
                    <label htmlFor="char-archetype">Archetype</label>
                    <input
                        id="char-archetype"
                        placeholder="e.g. The Reluctant Hero"
                        value={newChar.archetype}
                        onChange={e => setNewChar({...newChar, archetype: e.target.value})}
                    />
                    {!editingId && !newChar.archetype && (
                        <button type="button" className="btn-generate" onClick={handleGenerate}>
                            ✨ Generate Traits
                        </button>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="char-motivation">Want (Motivation)</label>
                    <input
                        id="char-motivation"
                        value={newChar.motivation}
                        onChange={e => setNewChar({...newChar, motivation: e.target.value})}
                        placeholder="What drives them?"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="char-flaw">Need (Fatal Flaw)</label>
                    <input
                        id="char-flaw"
                        value={newChar.flaw}
                        onChange={e => setNewChar({...newChar, flaw: e.target.value})}
                        placeholder="What holds them back?"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="char-bio">Bio & Notes</label>
                    <textarea
                        id="char-bio"
                        rows={6}
                        value={newChar.bio}
                        onChange={e => setNewChar({...newChar, bio: e.target.value})}
                        placeholder="Backstory, physical description..."
                    />
                </div>

                <div className="drawer-footer">
                    <button
                        type="button"
                        className="btn-studio-secondary"
                        onClick={handleCancel}
                    >
                        Cancel
                    </button>
                    <button type="submit" className="btn-studio-primary" disabled={isSaving}>
                        {isSaving ? <Spinner size="small" color="white" /> : 'Save Profile'}
                    </button>
                </div>
            </form>
        </div>
      </div>
    </div>
  );
}
