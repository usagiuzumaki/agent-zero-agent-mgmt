import { useState } from 'react';
import { getTools } from '../plugins';

/**
 * Chat panel with message list, input box and plugin action buttons.
 */
export default function AgentChat({ onLog }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const tools = getTools();

  const sendMessage = () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages([...messages, userMsg]);
    onLog && onLog(`user: ${input}`);
    setInput('');
  };

  const handleTool = (tool) => {
    tool.action((msg) => {
      setMessages((prev) => [...prev, { sender: 'agent', text: msg }]);
      onLog && onLog(`agent: ${msg}`);
    });
  };

  return (
    <div className="agent-chat">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg msg-${m.sender}`}>{m.text}</div>
        ))}
      </div>
      <div className="tool-bar">
        {tools.map((tool) => (
          <button key={tool.name} onClick={() => handleTool(tool)}>
            {tool.label}
          </button>
        ))}
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
