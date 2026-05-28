import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { HandshakeIcon, AlertCircle, Clock } from 'lucide-react';

interface Grievance {
  grievance_id: string;
  filed_by: string;
  category: string;
  status: string;
  priority: string;
  filed_at: string;
  description: string;
}

export default function RelationsPage() {
  const [grievances, setGrievances] = useState<Grievance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/relations/')
      .then(res => res.json())
      .then(data => {
        setGrievances(data);
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
        <div className="page-header__icon" style={{ color: '#f97316', backgroundColor: 'rgba(249, 115, 22, 0.1)' }}>
          <HandshakeIcon size={24} />
        </div>
        <div>
          <h1 className="page-title">Employee Relations</h1>
          <p className="page-subtitle">Manage cases and employee grievances</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : grievances.length === 0 ? (
        <div className="empty-state">No open cases at this time.</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Filed Date</th>
              </tr>
            </thead>
            <tbody>
              {grievances.map(g => (
                <tr key={g.grievance_id}>
                  <td className="font-medium text-orange-400">{g.grievance_id}</td>
                  <td className="capitalize">{g.category.replace('_', ' ')}</td>
                  <td>
                    <span className={`px-2 py-1 rounded text-xs ${g.priority === 'High' ? 'bg-red-500/10 text-red-500' : 'bg-yellow-500/10 text-yellow-500'}`}>
                      {g.priority}
                    </span>
                  </td>
                  <td>{g.status}</td>
                  <td><span className="flex items-center gap-1 text-slate-400"><Clock size={12}/> {new Date(g.filed_at).toLocaleDateString()}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </motion.div>
  );
}
