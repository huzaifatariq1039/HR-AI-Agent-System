import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Heart, Star } from 'lucide-react';

interface Recognition {
  recognition_id: string;
  recipient_id: string;
  sender: string;
  message: string;
  category: string;
  created_at: string;
  points_awarded: number;
}

export default function EngagementPage() {
  const [recognitions, setRecognitions] = useState<Recognition[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/engagement/')
      .then(res => res.json())
      .then(data => {
        setRecognitions(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="page-container"
    >
      <div className="page-header">
        <div className="page-header__icon" style={{ color: '#a855f7', backgroundColor: 'rgba(168, 85, 247, 0.1)' }}>
          <Heart size={24} />
        </div>
        <div>
          <h1 className="page-title">Engagement & Kudos</h1>
          <p className="page-subtitle">Employee recognition and shout-outs</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : recognitions.length === 0 ? (
        <div className="empty-state">No recognitions yet. Be the first to send one!</div>
      ) : (
        <div className="grid-cards">
          {recognitions.map(rec => (
            <div key={rec.recognition_id} className="card bg-gradient-to-br from-slate-800 to-purple-900/20 border-purple-500/20">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400">
                    <Star size={16} />
                  </div>
                  <div>
                    <div className="font-medium text-purple-300">{rec.recipient_id}</div>
                    <div className="text-xs text-slate-400">From: {rec.sender}</div>
                  </div>
                </div>
                <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-1 rounded capitalize">
                  {rec.category}
                </span>
              </div>
              <p className="text-slate-300 text-sm mb-4">"{rec.message}"</p>
              <div className="flex justify-between items-center text-xs text-slate-500 border-t border-purple-500/20 pt-3">
                <span>{new Date(rec.created_at).toLocaleDateString()}</span>
                <span className="text-amber-400 font-medium">+{rec.points_awarded} pts</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
