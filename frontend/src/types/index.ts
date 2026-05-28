/**
 * TypeScript type definitions for the HR AI Agent System frontend.
 */

/** A single chat message (user or agent). */
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: ToolEvent[];
  isStreaming?: boolean;
}

/** Represents a tool invocation event. */
export interface ToolEvent {
  toolName: string;
  status: 'running' | 'completed' | 'error';
  input?: Record<string, string>;
  result?: string;
}

/**
 * A single frame received from the WebSocket stream.
 *
 * Types:
 * - `token`      — a chunk of the agent's text response
 * - `tool_start` — the agent is invoking a specific tool
 * - `tool_end`   — the tool has finished executing
 * - `error`      — an error occurred during processing
 * - `done`       — the agent has finished its response
 */
export interface StreamFrame {
  type: 'token' | 'tool_start' | 'tool_end' | 'error' | 'done';
  data: string;
  tool_name?: string;
  metadata?: Record<string, unknown>;
}

/** Overall chat state managed by the ChatWindow component. */
export interface ChatState {
  messages: Message[];
  isConnected: boolean;
  isLoading: boolean;
  activeTools: ToolEvent[];
  error: string | null;
}

/** HR tool category for sidebar display. */
export interface ToolCategory {
  name: string;
  icon: string;
  tools: string[];
  color: string;
}
