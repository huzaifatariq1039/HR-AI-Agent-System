import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Users, UserMinus, Building } from 'lucide-react';

interface Metrics {
  total_headcount: number;
  active_employees: number;
  on_leave: number;
  company_avg_tenure_years: number;
  overall_attrition_rate: string;
  departments: Record<string, any>;
  report_date: string;
}

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/analytics/')
      .then(res => res.json())
      .then(data => {
        setMetrics(data);
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
        <div className="page-header__icon" style={{ color: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)' }}>
          <BarChart3 size={24} />
        </div>
        <div>
          <h1 className="page-title">Analytics</h1>
          <p className="page-subtitle">Workforce metrics and insights</p>
        </div>
      </div>

      {loading || !metrics ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-slate-400 text-sm">Total Headcount</div>
                  <div className="text-3xl font-semibold text-blue-400 mt-1">{metrics.total_headcount}</div>
                </div>
                <Users size={24} className="text-blue-500/50" />
              </div>
            </div>
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-slate-400 text-sm">Active</div>
                  <div className="text-3xl font-semibold text-emerald-400 mt-1">{metrics.active_employees}</div>
                </div>
                <Building size={24} className="text-emerald-500/50" />
              </div>
            </div>
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-slate-400 text-sm">On Leave</div>
                  <div className="text-3xl font-semibold text-amber-400 mt-1">{metrics.on_leave}</div>
                </div>
                <Users size={24} className="text-amber-500/50" />
              </div>
            </div>
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-slate-400 text-sm">Attrition</div>
                  <div className="text-3xl font-semibold text-rose-400 mt-1">{metrics.overall_attrition_rate}</div>
                </div>
                <UserMinus size={24} className="text-rose-500/50" />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/30 p-6 rounded-xl border border-slate-700/50">
            <h3 className="text-lg font-medium mb-4">Department Breakdown</h3>
            <div className="table-container bg-transparent border-0 p-0">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Department</th>
                    <th>Headcount</th>
                    <th>Open Roles</th>
                    <th>Avg Tenure</th>
                    <th>Attrition</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(metrics.departments).map(([dept, data]: [string, any]) => (
                    <tr key={dept}>
                      <td className="font-medium">{dept}</td>
                      <td>{data.headcount}</td>
                      <td>{data.open_positions}</td>
                      <td>{data.avg_tenure_years} yrs</td>
                      <td>{data.attrition_rate}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
}
