import { useState } from 'react';
import AgentLauncher from './components/AgentLauncher';
import AgentModal from './components/AgentModal';
import AgentChat from './components/AgentChat';
import AgentLogView from './components/AgentLogView';
import ScreenwritingUI from './components/ScreenwritingUI';
import EgirlUI from './components/EgirlUI';
import config from '../agent.config.json';

export default function App() {
  const [open, setOpen] = useState(false);
  const [logs, setLogs] = useState([]);
  const [ui, setUI] = useState('default');
  const [theme, setTheme] = useState(config.theme || 'aurora');

  const handleLog = (log) => {
    setLogs((prev) => [...prev, log]);
  };

  const renderUI = () => {
    switch (ui) {
      case 'screenwriting':
        return <ScreenwritingUI onLog={handleLog} />;
      case 'egirl':
        return <EgirlUI onLog={handleLog} />;
      default:
        return <AgentChat onLog={handleLog} />;
    }
  };

  return (
    <div className="app-container" data-theme={theme}>
      <AgentLauncher onOpen={() => setOpen(true)} />
      <AgentModal
        open={open}
        onClose={() => setOpen(false)}
        className={ui === 'screenwriting' ? 'full-screen' : ''}
      >
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <select
            className="ui-select"
            value={ui}
            onChange={(e) => setUI(e.target.value)}
            style={{ flex: 1, marginBottom: 0 }}
            aria-label="Select Interface Mode"
            title="Select Interface Mode"
          >
            <option value="default">Default</option>
            <option value="screenwriting">Screenwriting</option>
            <option value="egirl">Aria</option>
          </select>
          <select
            className="ui-select"
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            style={{ flex: 1, marginBottom: 0 }}
            aria-label="Select Theme"
            title="Select Theme"
          >
            <option value="aurora">Aurora (Aria)</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="casino">Story Casino</option>
            <option value="storybook">Living Storybook</option>
            <option value="terminal">Arcane Terminal</option>
          </select>
        </div>
        {renderUI()}
        <AgentLogView logs={logs} />
      </AgentModal>
    </div>
  );
}
