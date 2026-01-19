import { memo } from 'react';

const MessageList = memo(({ messages, containerRef, messagesEndRef, onScroll }) => {
  return (
    <div
      className="messages"
      ref={containerRef}
      onScroll={onScroll}
    >
      {messages.map((m) => (
        <div key={m.id} className={`msg msg-${m.sender}`}>{m.text}</div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
});

export default MessageList;
