import { useState, useRef, useEffect, useCallback } from 'react';
import { getTools } from '../plugins';
import MessageList from './MessageList';
import Spinner from './common/Spinner';

/**
 * Chat panel with message list, input box and plugin action buttons.
 */
export default function AgentChat({ onLog }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [activeTool, setActiveTool] = useState(null);
  const tools = getTools();
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  // Scroll logic
  const containerRef = useRef(null);
  // Use useRef for tracking scroll state to avoid re-renders
  const isNearBottomRef = useRef(true);

  // Check if user is near bottom on scroll
  const handleScroll = useCallback(() => {
    const container = containerRef.current;
    if (container) {
      const { scrollTop, scrollHeight, clientHeight } = container;
      // 50px threshold to determine if "near bottom"
      const bottom = scrollHeight - scrollTop - clientHeight < 50;
      isNearBottomRef.current = bottom;
    }
  }, []);

  // Scroll to bottom when messages change, IF we were already near bottom
  useEffect(() => {
    if (isNearBottomRef.current && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

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
    isNearBottomRef.current = true;
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim()) {
        sendMessage();
      }
    }
  };

  const handleTool = async (tool) => {
    if (activeTool) return;
    setActiveTool(tool.name);
    try {
      await tool.action((msg) => {
        setMessages((prev) => [
          ...prev,
          { id: crypto.randomUUID(), sender: 'agent', text: msg },
        ]);
        onLog && onLog(`agent: ${msg}`);
      });
    } finally {
      setActiveTool(null);
    }
  };

  return (
    <div className="agent-chat">
      <div
        className="messages"
        ref={containerRef}
        onScroll={handleScroll}
      >
        <MessageList messages={messages} bottomRef={messagesEndRef} />
      </div>
      <div className="tool-bar">
        {tools.map((tool) => (
          <button
            key={tool.name}
            onClick={() => handleTool(tool)}
            disabled={!!activeTool}
            aria-busy={activeTool === tool.name}
            style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}
          >
            {activeTool === tool.name && <Spinner size="small" />}
            {tool.label}
          </button>
        ))}
      </div>
      <div className="input-row">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message (Shift+Enter for new line)"
          aria-label="Message input"
          rows={1}
          style={{ overflow: 'hidden', resize: 'none' }}
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          aria-label="Send message"
          title="Send message"
          className="send-btn"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  );
}
