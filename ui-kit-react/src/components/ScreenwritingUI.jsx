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
        <div className="tab-nav" role="tablist" aria-label="Screenwriting sections">
          <button
            id="tab-assistant"
            role="tab"
            aria-selected={activeTab === 'assistant'}
            aria-controls="panel-assistant"
            className={`tab-btn ${activeTab === 'assistant' ? 'active' : ''}`}
            onClick={() => setActiveTab('assistant')}
          >
            Assistant
          </button>
          <button
            id="tab-storybook"
            role="tab"
            aria-selected={activeTab === 'storybook'}
            aria-controls="panel-storybook"
            className={`tab-btn ${activeTab === 'storybook' ? 'active' : ''}`}
            onClick={() => setActiveTab('storybook')}
          >
            Storybook
          </button>
          <button
            id="tab-characters"
            role="tab"
            aria-selected={activeTab === 'characters'}
            aria-controls="panel-characters"
            className={`tab-btn ${activeTab === 'characters' ? 'active' : ''}`}
            onClick={() => setActiveTab('characters')}
          >
            Characters
          </button>
        </div>
      </div>

      <div className="screenwriting-body">
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
      </div>
    </div>
  );
}
