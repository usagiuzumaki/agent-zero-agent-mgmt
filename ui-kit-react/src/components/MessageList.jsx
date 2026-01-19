import { memo } from 'react';

const MessageList = memo(({ messages, bottomRef }) => {
  return (
    <>
      {messages.map((m) => (
        <div key={m.id} className={`msg msg-${m.sender}`}>
          {m.text}
        </div>
      ))}
      <div ref={bottomRef} />
    </>
  );
});

MessageList.displayName = 'MessageList';

export default MessageList;
