import { useState, useRef, useEffect } from 'react';
import { getTools } from '../plugins';

/**
 * Chat panel with message list, input box and plugin action buttons.
 */
export default function AgentChat({ onLog }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const tools = getTools();

  // Scroll logic
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  const [isNearBottom, setIsNearBottom] = useState(true);

  // Check if user is near bottom on scroll
  const handleScroll = () => {
    const container = containerRef.current;
    if (container) {
      const { scrollTop, scrollHeight, clientHeight } = container;
      // 50px threshold to determine if "near bottom"
      const bottom = scrollHeight - scrollTop - clientHeight < 50;
      setIsNearBottom(bottom);
    }
  };

  // Scroll to bottom when messages change, IF we were already near bottom
  useEffect(() => {
    if (isNearBottom && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isNearBottom]);


  const sendMessage = () => {
    if (!input.trim()) return;
    const text = input;
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), sender: 'user', text },
    ]);
    onLog && onLog(`user: ${text}`);
    setInput('');
    // Ensure we scroll to bottom when user sends a message
    setIsNearBottom(true);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim()) {
        sendMessage();
      }
    }
  };

  const handleTool = (tool) => {
    tool.action((msg) => {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), sender: 'agent', text: msg },
      ]);
      onLog && onLog(`agent: ${msg}`);
    });
  };

  return (
    <div className="agent-chat">
      <div
        className="messages"
        ref={containerRef}
        onScroll={handleScroll}
        role="log"
        aria-live="polite"
        aria-label="Chat history"
        tabIndex={0}
        style={{ minHeight: '200px' }}
      >
        {messages.length === 0 && (
          <div className="empty-state" style={{ padding: '1rem', color: 'var(--color-text-muted)', textAlign: 'center' }}>
            Start a conversation...
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`msg msg-${m.sender}`}>{m.text}</div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="tool-bar">
        {tools.map((tool) => (
          <button key={tool.name} onClick={() => handleTool(tool)}>
            {tool.label}
          </button>
        ))}
      </div>
      <div className="input-row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message (Shift+Enter for new line)"
          aria-label="Message input"
          rows={3}
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
}
