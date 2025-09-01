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
    <div className="app-container" data-theme={config.theme || 'light'}>
      <AgentLauncher onOpen={() => setOpen(true)} />
      <AgentModal open={open} onClose={() => setOpen(false)}>
        <select
          className="ui-select"
          value={ui}
          onChange={(e) => setUI(e.target.value)}
        >
          <option value="default">Default</option>
          <option value="screenwriting">Screenwriting</option>
          <option value="egirl">E-Girl</option>
        </select>
        {renderUI()}
        <AgentLogView logs={logs} />
      </AgentModal>
    </div>
  );
}
