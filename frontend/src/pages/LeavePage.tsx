import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CalendarDays } from 'lucide-react';

interface LeaveBalance {
  employee_id: string;
  employee_name: string;
  fiscal_year: string;
  balances: Record<string, { total: number; used: number; remaining: number }>;
}

export default function LeavePage() {
  const [balances, setBalances] = useState<LeaveBalance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/leave/balances')
      .then(res => res.json())
      .then(data => {
        setBalances(data);
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
        <div className="page-header__icon" style={{ color: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)' }}>
          <CalendarDays size={24} />
        </div>
        <div>
          <h1 className="page-title">Leave & Attendance</h1>
          <p className="page-subtitle">Track time off and employee availability</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="grid-cards">
          {balances.map(b => (
            <div key={b.employee_id} className="card">
              <div className="card-header">
                <h3 className="card-title">{b.employee_name}</h3>
                <span className="text-sm text-slate-400">FY {b.fiscal_year}</span>
              </div>
              <div className="mt-4 space-y-3">
                {Object.entries(b.balances).map(([type, stats]) => (
                  <div key={type} className="flex flex-col gap-1">
                    <div className="flex justify-between text-sm">
                      <span className="capitalize">{type.replace('_', ' ')}</span>
                      <span className="font-medium text-amber-500">{stats.remaining} days left</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5">
                      <div 
                        className="bg-amber-500 h-1.5 rounded-full" 
                        style={{ width: `${(stats.used / stats.total) * 100}%` }}
                      ></div>
                    </div>
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
