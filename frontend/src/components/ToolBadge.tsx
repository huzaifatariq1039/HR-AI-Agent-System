/**
 * ToolBadge — Visual indicator showing which HR tool is being invoked.
 * Displays the tool name with a spinning loader or check icon based on status.
 */

import { motion } from 'framer-motion';
import { Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import type { ToolEvent } from '../types';

/** Map tool function names to human-readable category labels and colors. */
const TOOL_DISPLAY: Record<string, { label: string; color: string }> = {
  create_job_posting:    { label: '📋 Recruitment',       color: '#6366f1' },
  list_job_postings:     { label: '📋 Recruitment',       color: '#6366f1' },
  get_employee_profile:  { label: '👤 Employee Records',  color: '#8b5cf6' },
  search_employees:      { label: '👤 Employee Records',  color: '#8b5cf6' },
  get_onboarding_status: { label: '🚀 Onboarding',       color: '#06b6d4' },
  get_payslip_summary:   { label: '💰 Payroll',           color: '#10b981' },
  apply_leave:           { label: '🏖️ Leave',             color: '#f59e0b' },
  get_leave_balance:     { label: '🏖️ Leave',             color: '#f59e0b' },
  get_goals:             { label: '🎯 Performance',       color: '#ec4899' },
  list_training_programs:{ label: '📚 Training',          color: '#14b8a6' },
  file_grievance:        { label: '🤝 Relations',         color: '#f97316' },
  get_policy:            { label: '📜 Compliance',        color: '#64748b' },
  get_headcount_metrics: { label: '📊 Analytics',         color: '#3b82f6' },
  send_recognition:      { label: '🌟 Engagement',        color: '#a855f7' },
};

interface ToolBadgeProps {
  tool: ToolEvent;
}

export default function ToolBadge({ tool }: ToolBadgeProps) {
  const display = TOOL_DISPLAY[tool.toolName] || { label: `🔧 ${tool.toolName}`, color: '#6366f1' };
  const isRunning = tool.status === 'running';
  const isError = tool.status === 'error';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8, y: 8 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
      className="tool-badge"
      style={{ '--tool-color': display.color } as React.CSSProperties}
    >
      <span className="tool-badge__icon">
        {isRunning && <Loader2 size={14} className="animate-spin" />}
        {tool.status === 'completed' && <CheckCircle2 size={14} />}
        {isError && <AlertCircle size={14} />}
      </span>
      <span className="tool-badge__label">{display.label}</span>
      {isRunning && (
        <motion.span
          className="tool-badge__dots"
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1.2, repeat: Infinity }}
        >
          processing...
        </motion.span>
      )}
    </motion.div>
  );
}
