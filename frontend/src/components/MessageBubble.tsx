/**
 * MessageBubble — Renders a single chat message with distinct styling
 * for user vs. agent messages, markdown rendering, and tool badges.
 */

import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Bot } from 'lucide-react';
import ToolBadge from './ToolBadge';
import type { Message } from '../types';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 16, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: 'spring', stiffness: 300, damping: 28 }}
      className={`message ${isUser ? 'message--user' : 'message--assistant'}`}
    >
      {/* Avatar */}
      <div className={`message__avatar ${isUser ? 'message__avatar--user' : 'message__avatar--assistant'}`}>
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>

      {/* Content */}
      <div className={`message__content ${isUser ? 'message__content--user' : 'message__content--assistant'}`}>
        {/* Tool badges (agent only) */}
        {!isUser && message.toolCalls && message.toolCalls.length > 0 && (
          <div className="message__tools">
            {message.toolCalls.map((tool, index) => (
              <ToolBadge key={`${tool.toolName}-${index}`} tool={tool} />
            ))}
          </div>
        )}

        {/* Message text */}
        <div className="message__text">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                // Style code blocks
                code({ className, children, ...props }) {
                  const isInline = !className;
                  if (isInline) {
                    return <code className="inline-code" {...props}>{children}</code>;
                  }
                  return (
                    <pre className="code-block">
                      <code className={className} {...props}>{children}</code>
                    </pre>
                  );
                },
                // Style tables
                table({ children, ...props }) {
                  return (
                    <div className="table-wrapper">
                      <table {...props}>{children}</table>
                    </div>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Streaming cursor */}
        {message.isStreaming && (
          <motion.span
            className="message__cursor"
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.5, repeat: Infinity }}
          >
            ▊
          </motion.span>
        )}

        {/* Timestamp */}
        <span className="message__time">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </motion.div>
  );
}
