/**
 * App — Root application component.
 * Manages session ID state and sidebar visibility.
 */

import { useState, useCallback } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';

// Pages
import RecruitmentPage from './pages/RecruitmentPage';
import RecordsPage from './pages/RecordsPage';
import OnboardingPage from './pages/OnboardingPage';
import PayrollPage from './pages/PayrollPage';
import LeavePage from './pages/LeavePage';
import PerformancePage from './pages/PerformancePage';
import TrainingPage from './pages/TrainingPage';
import RelationsPage from './pages/RelationsPage';
import CompliancePage from './pages/CompliancePage';
import AnalyticsPage from './pages/AnalyticsPage';
import EngagementPage from './pages/EngagementPage';

/** Generate a unique session ID. */
function generateSessionId(): string {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
}

export default function App() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState(generateSessionId);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedPrompt, setSelectedPrompt] = useState<string | undefined>(undefined);

  const handleNewChat = useCallback(() => {
    setSessionId(generateSessionId());
  }, []);

  return (
    <div className="app">
      <Sidebar
        onNewChat={handleNewChat}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onCategoryClick={(prompt) => {
          setSelectedPrompt(prompt);
          setSidebarOpen(false);
          navigate('/');
        }}
      />
      <div className="flex-1 flex overflow-hidden bg-transparent">
        <Routes>
          <Route path="/" element={<ChatWindow sessionId={sessionId} onToggleSidebar={() => setSidebarOpen((prev) => !prev)} selectedPrompt={selectedPrompt} onPromptConsumed={() => setSelectedPrompt(undefined)} />} />
          <Route path="/recruitment" element={<RecruitmentPage />} />
          <Route path="/records" element={<RecordsPage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/payroll" element={<PayrollPage />} />
          <Route path="/leave" element={<LeavePage />} />
          <Route path="/performance" element={<PerformancePage />} />
          <Route path="/training" element={<TrainingPage />} />
          <Route path="/relations" element={<RelationsPage />} />
          <Route path="/compliance" element={<CompliancePage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/engagement" element={<EngagementPage />} />
        </Routes>
      </div>
    </div>
  );
}
