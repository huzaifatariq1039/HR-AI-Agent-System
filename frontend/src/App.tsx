/**
 * App — Root application component.
 * Manages session ID state and sidebar visibility.
 */

import { useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';

/** Generate a unique session ID. */
function generateSessionId(): string {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
}

export default function App() {
  const [sessionId, setSessionId] = useState(generateSessionId);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNewChat = useCallback(() => {
    setSessionId(generateSessionId());
  }, []);

  return (
    <div className="app">
      <Sidebar
        onNewChat={handleNewChat}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <ChatWindow
        sessionId={sessionId}
        onToggleSidebar={() => setSidebarOpen((prev) => !prev)}
      />
    </div>
  );
}
