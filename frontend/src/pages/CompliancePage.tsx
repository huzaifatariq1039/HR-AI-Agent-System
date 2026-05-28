import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, FileText } from 'lucide-react';

interface Policy {
  id: string;
  title: string;
  category: string;
  version: string;
  last_updated: string;
  summary: string;
  key_points: string[];
}

export default function CompliancePage() {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/compliance/')
      .then(res => res.json())
      .then(data => {
        setPolicies(data);
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
        <div className="page-header__icon" style={{ color: '#64748b', backgroundColor: 'rgba(100, 116, 139, 0.1)' }}>
          <ShieldCheck size={24} />
        </div>
        <div>
          <h1 className="page-title">Compliance & Policies</h1>
          <p className="page-subtitle">Company handbooks and regulations</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="grid-cards">
          {policies.map(policy => (
            <div key={policy.id} className="card">
              <div className="card-header border-b border-slate-800 pb-3 mb-3">
                <h3 className="card-title">{policy.title}</h3>
                <span className="text-xs text-slate-400 bg-slate-800 px-2 py-1 rounded">v{policy.version}</span>
              </div>
              <p className="card-text mb-4 text-sm">{policy.summary}</p>
              
              <div className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wider">Key Points</div>
              <ul className="space-y-1 mb-4">
                {policy.key_points.slice(0, 3).map((pt, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <FileText size={14} className="mt-0.5 text-slate-500 min-w-max"/> {pt}
                  </li>
                ))}
              </ul>
              
              <div className="text-xs text-slate-500 pt-3 border-t border-slate-800">
                Last updated: {policy.last_updated}
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
