import { useState } from 'react';
import AgentLauncher from './components/AgentLauncher';
import AgentModal from './components/AgentModal';
import AgentChat from './components/AgentChat';
import AgentLogView from './components/AgentLogView';
import config from '../agent.config.json';

export default function App() {
  const [open, setOpen] = useState(false);
  const [logs, setLogs] = useState([]);

  return (
    <div className="app-container" data-theme={config.theme || 'light'}>
      <AgentLauncher onOpen={() => setOpen(true)} />
      <AgentModal open={open} onClose={() => setOpen(false)}>
        <AgentChat onLog={(log) => setLogs((prev) => [...prev, log])} />
        <AgentLogView logs={logs} />
      </AgentModal>
    </div>
  );
}
