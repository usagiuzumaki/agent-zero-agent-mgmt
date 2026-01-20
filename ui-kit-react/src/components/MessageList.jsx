import React, { memo } from 'react';

const MessageList = memo(({ messages, containerRef, onScroll, messagesEndRef }) => {
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
