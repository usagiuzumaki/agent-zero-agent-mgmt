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
  const textareaRef = useRef(null);
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

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      // Reset height to auto to calculate correct scrollHeight
      textareaRef.current.style.height = 'auto';

      const scrollHeight = textareaRef.current.scrollHeight;
      // Set new height based on scrollHeight, capped at 150px
      const newHeight = Math.min(scrollHeight, 150);
      textareaRef.current.style.height = `${newHeight}px`;

      // Show scrollbar only if content exceeds max height
      textareaRef.current.style.overflowY = scrollHeight > 150 ? 'auto' : 'hidden';
    }
  }, [input]);

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
      >
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
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          aria-label="Message input"
          rows={1}
          style={{
            minHeight: '40px',
            maxHeight: '150px',
            resize: 'none',
            overflowY: 'hidden' // Initial state, updated by useEffect
          }}
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          aria-label="Send message"
          title="Send message"
          style={{
            height: '40px',
            width: '40px',
            padding: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '50%' // Make it circular for the icon
          }}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M22 2L11 13"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M22 2L15 22L11 13L2 9L22 2Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
