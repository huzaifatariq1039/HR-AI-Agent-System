/**
 * ChatWindow — Core chat component managing the conversation with the HR AI Agent.
 *
 * Features:
 * - WebSocket connection for streaming responses
 * - Auto-scroll to latest messages
 * - Input bar with send button
 * - Typing indicator during agent processing
 * - Tool invocation badges
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Wifi, WifiOff, Menu, Sparkles } from 'lucide-react';
import { ChatWebSocket } from '../services/api';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import type { Message, ToolEvent } from '../types';

interface ChatWindowProps {
  sessionId: string;
  onToggleSidebar: () => void;
}

/** Generate a unique message ID. */
function generateId(): string {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export default function ChatWindow({ sessionId, onToggleSidebar }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [activeTools, setActiveTools] = useState<ToolEvent[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const wsRef = useRef<ChatWebSocket | null>(null);
  const streamingMessageRef = useRef<string>('');
  const streamingIdRef = useRef<string>('');
  const toolCallsRef = useRef<ToolEvent[]>([]);

  /** Scroll to the bottom of the messages list. */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  /** Initialize WebSocket connection. */
  useEffect(() => {
    const ws = new ChatWebSocket({
      onToken(token: string) {
        streamingMessageRef.current += token;
        setMessages((prev) => {
          const updated = [...prev];
          const lastIdx = updated.findIndex((m) => m.id === streamingIdRef.current);
          if (lastIdx !== -1) {
            updated[lastIdx] = {
              ...updated[lastIdx],
              content: streamingMessageRef.current,
              isStreaming: true,
            };
          }
          return updated;
        });
      },

      onToolStart(toolName: string, metadata?: Record<string, unknown>) {
        const toolEvent: ToolEvent = { toolName, status: 'running', input: metadata as Record<string, string> | undefined };
        toolCallsRef.current = [...toolCallsRef.current, toolEvent];
        setActiveTools((prev) => [...prev, toolEvent]);
        // Update the streaming message's tool calls
        setMessages((prev) => {
          const updated = [...prev];
          const lastIdx = updated.findIndex((m) => m.id === streamingIdRef.current);
          if (lastIdx !== -1) {
            updated[lastIdx] = { ...updated[lastIdx], toolCalls: [...toolCallsRef.current] };
          }
          return updated;
        });
      },

      onToolEnd(toolName: string, result: string) {
        toolCallsRef.current = toolCallsRef.current.map((t) =>
          t.toolName === toolName && t.status === 'running'
            ? { ...t, status: 'completed' as const, result }
            : t
        );
        setActiveTools((prev) =>
          prev.map((t) =>
            t.toolName === toolName && t.status === 'running'
              ? { ...t, status: 'completed', result }
              : t
          )
        );
        // Update the streaming message's tool calls
        setMessages((prev) => {
          const updated = [...prev];
          const lastIdx = updated.findIndex((m) => m.id === streamingIdRef.current);
          if (lastIdx !== -1) {
            updated[lastIdx] = { ...updated[lastIdx], toolCalls: [...toolCallsRef.current] };
          }
          return updated;
        });
      },

      onDone() {
        setMessages((prev) =>
          prev.map((m) => (m.id === streamingIdRef.current ? { ...m, isStreaming: false } : m))
        );
        setIsLoading(false);
        setActiveTools([]);
        streamingMessageRef.current = '';
        toolCallsRef.current = [];
      },

      onError(error: string) {
        console.error('Agent error:', error);
        setIsLoading(false);
        setActiveTools([]);
        // Add error as agent message
        if (streamingIdRef.current) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === streamingIdRef.current
                ? { ...m, content: m.content || `⚠️ Error: ${error}`, isStreaming: false }
                : m
            )
          );
        }
      },

      onConnectionChange(connected: boolean) {
        setIsConnected(connected);
      },
    });

    ws.connect();
    wsRef.current = ws;

    return () => ws.disconnect();
  }, [sessionId]);

  /** Send a message to the agent. */
  const handleSend = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    // Add user message
    const userMsg: Message = {
      id: generateId(),
      role: 'user',
      content: trimmed,
      timestamp: new Date(),
    };

    // Prepare assistant placeholder
    const assistantId = generateId();
    streamingIdRef.current = assistantId;
    streamingMessageRef.current = '';
    toolCallsRef.current = [];

    const assistantMsg: Message = {
      id: assistantId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      toolCalls: [],
      isStreaming: true,
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setInput('');
    setIsLoading(true);

    wsRef.current?.send(trimmed, sessionId);
    inputRef.current?.focus();
  }, [input, isLoading, sessionId]);

  /** Handle Enter key (Shift+Enter for newline). */
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="chat-window">
      {/* Header */}
      <header className="chat-window__header">
        <button className="chat-window__menu-btn" onClick={onToggleSidebar}>
          <Menu size={20} />
        </button>
        <div className="chat-window__header-info">
          <h2 className="chat-window__header-title">HR Assistant</h2>
          <span className={`chat-window__connection ${isConnected ? 'chat-window__connection--active' : ''}`}>
            {isConnected ? <Wifi size={12} /> : <WifiOff size={12} />}
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </header>

      {/* Messages area */}
      <div className="chat-window__messages">
        {isEmpty && (
          <motion.div
            className="chat-window__empty"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="chat-window__empty-icon">
              <Sparkles size={48} />
            </div>
            <h3 className="chat-window__empty-title">HR AI Assistant</h3>
            <p className="chat-window__empty-subtitle">
              Your complete AI-powered HR department. Ask me anything about recruitment, employee records, leave, payroll, and more.
            </p>
            <div className="chat-window__suggestions">
              {[
                'Show all open job postings',
                "What's the leave balance for EMP-001?",
                'List available training programs',
                'Get the headcount metrics',
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  className="chat-window__suggestion"
                  onClick={() => { setInput(suggestion); inputRef.current?.focus(); }}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
        </AnimatePresence>

        {isLoading && activeTools.length === 0 && !messages.find((m) => m.isStreaming && m.content) && (
          <TypingIndicator />
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <div className="chat-window__input-bar">
        <div className="chat-window__input-container">
          <textarea
            ref={inputRef}
            id="chat-input"
            className="chat-window__input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything about HR..."
            rows={1}
            disabled={isLoading}
          />
          <button
            className="chat-window__send-btn"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </div>
        <p className="chat-window__disclaimer">
          HR AI Agent uses GPT-4o. Verify important information with your HR team.
        </p>
      </div>
    </div>
  );
}
