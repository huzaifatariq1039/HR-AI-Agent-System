/**
 * API Service — WebSocket & REST communication with the HR AI Agent backend.
 *
 * Handles:
 * - WebSocket connection lifecycle (connect, reconnect, send)
 * - Streaming frame parsing (token, tool_start, tool_end, done, error)
 * - Fallback REST endpoint for non-streaming chat
 */

import type { StreamFrame } from '../types';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/api/ws/chat';
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// ---------------------------------------------------------------------------
// WebSocket manager
// ---------------------------------------------------------------------------

export interface WebSocketHandlers {
  onToken: (token: string) => void;
  onToolStart: (toolName: string, metadata?: Record<string, unknown>) => void;
  onToolEnd: (toolName: string, result: string) => void;
  onDone: () => void;
  onError: (error: string) => void;
  onConnectionChange: (connected: boolean) => void;
}

export class ChatWebSocket {
  private ws: WebSocket | null = null;
  private handlers: WebSocketHandlers;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(handlers: WebSocketHandlers) {
    this.handlers = handlers;
  }

  /** Establish a WebSocket connection. */
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket(WS_URL);

    this.ws.onopen = () => {
      console.log('✅ WebSocket connected');
      this.reconnectAttempts = 0;
      this.handlers.onConnectionChange(true);
    };

    this.ws.onmessage = (event: MessageEvent) => {
      try {
        const frame: StreamFrame = JSON.parse(event.data);
        this.handleFrame(frame);
      } catch (err) {
        console.error('Failed to parse WebSocket frame:', err);
      }
    };

    this.ws.onclose = () => {
      console.log('❌ WebSocket disconnected');
      this.handlers.onConnectionChange(false);
      this.attemptReconnect();
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      this.handlers.onError('WebSocket connection error');
    };
  }

  /** Send a user message through the WebSocket. */
  send(message: string, sessionId: string): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.handlers.onError('Not connected to server. Attempting to reconnect...');
      this.connect();
      return;
    }

    this.ws.send(JSON.stringify({ message, session_id: sessionId }));
  }

  /** Cleanly close the connection. */
  disconnect(): void {
    this.maxReconnectAttempts = 0; // prevent reconnect
    this.ws?.close();
    this.ws = null;
  }

  // ── Internal ──────────────────────────────────────────────────────────

  private handleFrame(frame: StreamFrame): void {
    switch (frame.type) {
      case 'token':
        this.handlers.onToken(frame.data);
        break;
      case 'tool_start':
        this.handlers.onToolStart(frame.tool_name || 'unknown', frame.metadata as Record<string, unknown> | undefined);
        break;
      case 'tool_end':
        this.handlers.onToolEnd(frame.tool_name || 'unknown', frame.data);
        break;
      case 'done':
        this.handlers.onDone();
        break;
      case 'error':
        this.handlers.onError(frame.data);
        break;
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})...`);

    setTimeout(() => this.connect(), delay);
  }
}

// ---------------------------------------------------------------------------
// REST fallback
// ---------------------------------------------------------------------------

export async function chatSync(message: string, sessionId: string): Promise<{
  reply: string;
  session_id: string;
  tool_calls: Array<{ name: string; args: Record<string, unknown> }>;
}> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.statusText}`);
  }

  return response.json();
}
