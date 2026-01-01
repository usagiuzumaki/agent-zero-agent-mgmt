import React, { useState } from 'react';
import AgentChat from './AgentChat';
import StorybookUI from './StorybookUI';
import CharactersUI from './CharactersUI';

export default function ScreenwritingUI({ onLog }) {
  const [activeTab, setActiveTab] = useState('assistant');

  return (
    <div className="screenwriting-ui">
      <div className="screenwriting-header">
        <h2>Screenwriting Studio</h2>
        <div className="tab-nav">
          <button
            className={`tab-btn ${activeTab === 'assistant' ? 'active' : ''}`}
            onClick={() => setActiveTab('assistant')}
          >
            Assistant
          </button>
          <button
            className={`tab-btn ${activeTab === 'storybook' ? 'active' : ''}`}
            onClick={() => setActiveTab('storybook')}
          >
            Storybook
          </button>
          <button
            className={`tab-btn ${activeTab === 'characters' ? 'active' : ''}`}
            onClick={() => setActiveTab('characters')}
          >
            Characters
          </button>
        </div>
      </div>

      <div className="screenwriting-body">
        {activeTab === 'assistant' && <AgentChat onLog={onLog} />}
        {activeTab === 'storybook' && <StorybookUI />}
        {activeTab === 'characters' && <CharactersUI />}
      </div>
    </div>
  );
}
