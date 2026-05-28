/**
 * Sidebar — Navigation panel with HR tool categories, branding, and new-chat button.
 */

import { motion } from 'framer-motion';
import { NavLink } from 'react-router-dom';
import {
  Briefcase, Users, Rocket, DollarSign, CalendarDays,
  Target, BookOpen, HandshakeIcon, ShieldCheck, BarChart3,
  Heart, MessageSquarePlus, Sparkles, X, Home
} from 'lucide-react';

interface SidebarProps {
  onNewChat: () => void;
  isOpen: boolean;
  onClose: () => void;
}

const TOOL_CATEGORIES = [
  { name: 'Recruitment',       path: '/recruitment', icon: Briefcase,     color: '#00ADB5' },
  { name: 'Employee Records',  path: '/records',     icon: Users,         color: '#00ADB5' },
  { name: 'Onboarding',        path: '/onboarding',  icon: Rocket,        color: '#00ADB5' },
  { name: 'Payroll',           path: '/payroll',     icon: DollarSign,    color: '#00ADB5' },
  { name: 'Leave & Attendance',path: '/leave',       icon: CalendarDays,  color: '#00ADB5' },
  { name: 'Performance',       path: '/performance', icon: Target,        color: '#00ADB5' },
  { name: 'Training',          path: '/training',    icon: BookOpen,      color: '#00ADB5' },
  { name: 'Relations',         path: '/relations',   icon: HandshakeIcon, color: '#00ADB5' },
  { name: 'Compliance',        path: '/compliance',  icon: ShieldCheck,   color: '#00ADB5' },
  { name: 'Analytics',         path: '/analytics',   icon: BarChart3,     color: '#00ADB5' },
  { name: 'Engagement',        path: '/engagement',  icon: Heart,         color: '#00ADB5' },
];

const CATEGORY_PROMPTS: Record<string, string> = {
  'Recruitment': 'Show me all open job postings.',
  'Employee Records': 'Search for an employee.',
  'Onboarding': 'Check the onboarding status for EMP-003.',
  'Payroll': 'Get the payslip summary for EMP-001.',
  'Leave & Attendance': 'What is the leave balance for EMP-001?',
  'Performance': 'Show the performance goals for EMP-001.',
  'Training': 'List available training programs.',
  'Relations': 'How do I file a grievance?',
  'Compliance': 'What is the remote work policy?',
  'Analytics': 'Get the headcount metrics.',
  'Engagement': 'I want to send a recognition to an employee.',
};

export default function Sidebar({ onNewChat, isOpen, onClose, onCategoryClick }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={onClose} />
      )}

      <motion.aside
        className={`sidebar ${isOpen ? 'sidebar--open' : ''}`}
        initial={false}
      >
        {/* Header */}
        <div className="sidebar__header">
          <div className="sidebar__brand">
            <Sparkles size={24} className="sidebar__brand-icon" />
            <div>
              <h1 className="sidebar__title">HR Agent</h1>
              <p className="sidebar__subtitle">AI-Powered HR System</p>
            </div>
          </div>
          <button className="sidebar__close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* New Chat button */}
        <button className="sidebar__new-chat" onClick={() => { onNewChat(); onClose(); }}>
          <MessageSquarePlus size={18} />
          <span>New Conversation</span>
        </button>

        {/* Dashboard Link */}
        <div className="sidebar__section-title mt-4">Dashboard</div>
        <nav className="sidebar__nav mb-4">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `sidebar__category ${isActive ? 'sidebar__category--active' : ''}`}
            onClick={onClose}
          >
            <div className="sidebar__category-icon" style={{ color: '#fff' }}>
              <Home size={16} />
            </div>
            <span className="sidebar__category-name">AI Assistant</span>
          </NavLink>
        </nav>

        {/* Tool categories */}
        <div className="sidebar__section-title">Capabilities</div>
        <nav className="sidebar__nav">
          {TOOL_CATEGORIES.map((cat, index) => {
            const Icon = cat.icon;
            return (
              <NavLink
                key={cat.name}
                to={cat.path}
                className={({ isActive }) => `sidebar__category ${isActive ? 'sidebar__category--active' : ''}`}
                onClick={onClose}
              >
                <div className="sidebar__category-icon" style={{ color: cat.color }}>
                  <Icon size={16} />
                </div>
                <span className="sidebar__category-name">{cat.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="sidebar__footer">
          <div className="sidebar__status">
            <span className="sidebar__status-dot" />
            <span>System Online</span>
          </div>
        </div>
      </motion.aside>
    </>
  );
}
