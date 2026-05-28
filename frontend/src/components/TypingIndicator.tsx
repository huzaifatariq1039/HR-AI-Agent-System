/**
 * TypingIndicator — Animated three-dot pulse indicator shown while the agent is processing.
 */

import { motion } from 'framer-motion';

export default function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="typing-indicator__avatar">
        <span className="typing-indicator__avatar-icon">🤖</span>
      </div>
      <div className="typing-indicator__bubble">
        <div className="typing-indicator__dots">
          {[0, 1, 2].map((i) => (
            <motion.span
              key={i}
              className="typing-indicator__dot"
              animate={{ y: [0, -6, 0] }}
              transition={{
                duration: 0.6,
                repeat: Infinity,
                delay: i * 0.15,
                ease: 'easeInOut',
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
