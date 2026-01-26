import React, { useState } from 'react';
import AgentChat from './AgentChat';
import StorybookUI from './StorybookUI';
import CharactersUI from './CharactersUI';
import './ScreenwritingUI.css';

export default function ScreenwritingUI({ onLog }) {
  const [activeTab, setActiveTab] = useState('assistant');

  return (
    <div className="screenwriting-ui">
      <nav className="studio-sidebar">
        <div className="studio-brand">
          <h2>Aria Studio</h2>
        </div>

        <div className="studio-nav" role="tablist" aria-label="Screenwriting sections">
          <button
            id="tab-assistant"
            role="tab"
            aria-selected={activeTab === 'assistant'}
            aria-controls="panel-assistant"
            className={`nav-item ${activeTab === 'assistant' ? 'active' : ''}`}
            onClick={() => setActiveTab('assistant')}
          >
            <span className="nav-icon">✨</span>
            Assistant
          </button>
          <button
            id="tab-storybook"
            role="tab"
            aria-selected={activeTab === 'storybook'}
            aria-controls="panel-storybook"
            className={`nav-item ${activeTab === 'storybook' ? 'active' : ''}`}
            onClick={() => setActiveTab('storybook')}
          >
            <span className="nav-icon">📖</span>
            Storybook
          </button>
          <button
            id="tab-characters"
            role="tab"
            aria-selected={activeTab === 'characters'}
            aria-controls="panel-characters"
            className={`nav-item ${activeTab === 'characters' ? 'active' : ''}`}
            onClick={() => setActiveTab('characters')}
          >
            <span className="nav-icon">👥</span>
            Characters
          </button>
        </div>

        <div className="studio-footer" style={{ marginTop: 'auto', fontSize: '0.8rem', color: 'var(--studio-text-muted)' }}>
          <p>Project: Untitled</p>
          <p>Status: Draft</p>
        </div>
      </nav>

      <main className="studio-content">
        {activeTab === 'assistant' && (
          <div role="tabpanel" id="panel-assistant" aria-labelledby="tab-assistant" tabIndex={0}>
            <AgentChat onLog={onLog} />
          </div>
        )}
        {activeTab === 'storybook' && (
          <div role="tabpanel" id="panel-storybook" aria-labelledby="tab-storybook" tabIndex={0}>
            <StorybookUI />
          </div>
        )}
        {activeTab === 'characters' && (
          <div role="tabpanel" id="panel-characters" aria-labelledby="tab-characters" tabIndex={0}>
            <CharactersUI />
          </div>
        )}
      </main>
    </div>
  );
}
