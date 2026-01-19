import { useState, useRef, useEffect, useCallback } from 'react';
import { getTools } from '../plugins';
import MessageList from './MessageList';

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
      {/*
        Optimization: MessageList is memoized to prevent re-rendering the entire
        message history on every keystroke (when 'input' state changes).
      */}
      <MessageList
        messages={messages}
        containerRef={containerRef}
        messagesEndRef={messagesEndRef}
        onScroll={handleScroll}
      />
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
