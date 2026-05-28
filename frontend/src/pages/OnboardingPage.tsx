import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Rocket, CheckCircle, Circle } from 'lucide-react';

interface OnboardingTask {
  task: string;
  completed: boolean;
  date: string | null;
}

interface OnboardingRecord {
  employee_id: string;
  employee_name: string;
  start_date: string;
  status: string;
  progress_percent: number;
  buddy: string;
  checklist: OnboardingTask[];
}

export default function OnboardingPage() {
  const [records, setRecords] = useState<OnboardingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/onboarding/')
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
        <div className="page-header__icon" style={{ color: '#06b6d4', backgroundColor: 'rgba(6, 182, 212, 0.1)' }}>
          <Rocket size={24} />
        </div>
        <div>
          <h1 className="page-title">Onboarding</h1>
          <p className="page-subtitle">Track new hire progress and checklists</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="grid-cards">
          {records.map(record => (
            <div key={record.employee_id} className="card">
              <div className="card-header">
                <h3 className="card-title">{record.employee_name}</h3>
                <span className="text-sm text-slate-400">{record.start_date}</span>
              </div>
              <div className="mt-2 mb-4">
                <div className="flex justify-between text-sm mb-1">
                  <span>Progress</span>
                  <span>{record.progress_percent}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${record.progress_percent}%` }}></div>
                </div>
              </div>
              <ul className="space-y-2 mt-4">
                {record.checklist.slice(0, 4).map((item, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-300">
                    {item.completed ? <CheckCircle size={14} className="text-emerald-500" /> : <Circle size={14} className="text-slate-600" />}
                    {item.task}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
