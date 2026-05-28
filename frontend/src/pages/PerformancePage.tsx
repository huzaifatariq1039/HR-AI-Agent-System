import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Target, TrendingUp } from 'lucide-react';

interface Goal {
  id: string;
  title: string;
  category: string;
  status: string;
  progress: number;
  due_date: string;
  key_results: string[];
}

interface PerformanceRecord {
  employee_id: string;
  employee_name: string;
  review_cycle: string;
  goals: Goal[];
}

export default function PerformancePage() {
  const [records, setRecords] = useState<PerformanceRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/performance/')
      .then(res => res.json())
      .then(data => {
        setRecords(data);
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
        <div className="page-header__icon" style={{ color: '#ec4899', backgroundColor: 'rgba(236, 72, 153, 0.1)' }}>
          <Target size={24} />
        </div>
        <div>
          <h1 className="page-title">Performance</h1>
          <p className="page-subtitle">Employee OKRs and goal tracking</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="space-y-6">
          {records.map(record => (
            <div key={record.employee_id} className="card">
              <div className="card-header border-b border-slate-800 pb-4 mb-4">
                <h3 className="card-title text-xl">{record.employee_name}</h3>
                <span className="text-sm font-medium px-2 py-1 bg-pink-500/10 text-pink-500 rounded">
                  {record.review_cycle}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {record.goals.map(goal => (
                  <div key={goal.id} className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-slate-200">{goal.title}</h4>
                      <span className="text-xs text-slate-400">{goal.due_date}</span>
                    </div>
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs px-2 py-0.5 bg-slate-700 rounded text-slate-300">{goal.category}</span>
                      <span className="text-xs text-pink-400">{goal.status}</span>
                    </div>
                    <div className="mb-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span>Progress</span>
                        <span>{goal.progress}%</span>
                      </div>
                      <div className="w-full bg-slate-900 rounded-full h-1.5">
                        <div className="bg-pink-500 h-1.5 rounded-full" style={{ width: `${goal.progress}%` }}></div>
                      </div>
                    </div>
                    <ul className="text-xs text-slate-400 space-y-1 mt-2">
                      {goal.key_results.map((kr, i) => (
                        <li key={i} className="flex items-start gap-1">
                          <TrendingUp size={12} className="mt-0.5 text-slate-500"/> {kr}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
