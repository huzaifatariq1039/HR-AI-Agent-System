/**
 * Sidebar — Navigation panel with HR tool categories, branding, and new-chat button.
 */

import { motion } from 'framer-motion';
import {
  Briefcase, Users, Rocket, DollarSign, CalendarDays,
  Target, BookOpen, HandshakeIcon, ShieldCheck, BarChart3,
  Heart, MessageSquarePlus, Sparkles, X,
} from 'lucide-react';

interface SidebarProps {
  onNewChat: () => void;
  isOpen: boolean;
  onClose: () => void;
}

const TOOL_CATEGORIES = [
  { name: 'Recruitment',       icon: Briefcase,     color: '#6366f1' },
  { name: 'Employee Records',  icon: Users,         color: '#8b5cf6' },
  { name: 'Onboarding',        icon: Rocket,        color: '#06b6d4' },
  { name: 'Payroll',           icon: DollarSign,    color: '#10b981' },
  { name: 'Leave & Attendance',icon: CalendarDays,  color: '#f59e0b' },
  { name: 'Performance',       icon: Target,        color: '#ec4899' },
  { name: 'Training',          icon: BookOpen,       color: '#14b8a6' },
  { name: 'Relations',         icon: HandshakeIcon, color: '#f97316' },
  { name: 'Compliance',        icon: ShieldCheck,   color: '#64748b' },
  { name: 'Analytics',         icon: BarChart3,     color: '#3b82f6' },
  { name: 'Engagement',        icon: Heart,         color: '#a855f7' },
];

export default function Sidebar({ onNewChat, isOpen, onClose }: SidebarProps) {
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

        {/* Tool categories */}
        <div className="sidebar__section-title">Capabilities</div>
        <nav className="sidebar__nav">
          {TOOL_CATEGORIES.map((cat, index) => {
            const Icon = cat.icon;
            return (
              <motion.div
                key={cat.name}
                className="sidebar__category"
                initial={{ opacity: 0, x: -16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.04 }}
              >
                <div className="sidebar__category-icon" style={{ color: cat.color }}>
                  <Icon size={16} />
                </div>
                <span className="sidebar__category-name">{cat.name}</span>
              </motion.div>
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
