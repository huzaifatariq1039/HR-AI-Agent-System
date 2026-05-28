import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Users, Mail, Phone, MapPin } from 'lucide-react';

interface Employee {
  id: string;
  name: string;
  email: string;
  department: string;
  position: string;
  manager: string;
  status: string;
  location: string;
  phone: string;
}

export default function RecordsPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/records/employees')
      .then(res => res.json())
      .then(data => {
        setEmployees(data);
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
        <div className="page-header__icon" style={{ color: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.1)' }}>
          <Users size={24} />
        </div>
        <div>
          <h1 className="page-title">Employee Records</h1>
          <p className="page-subtitle">Company directory and staff information</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Department</th>
                <th>Contact</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {employees.map(emp => (
                <tr key={emp.id}>
                  <td>
                    <div className="font-medium">{emp.name}</div>
                    <div className="text-xs text-slate-400">{emp.id}</div>
                  </td>
                  <td>{emp.position}</td>
                  <td>{emp.department}</td>
                  <td>
                    <div className="flex items-center gap-1 text-sm"><Mail size={12}/> {emp.email}</div>
                  </td>
                  <td>
                    <span className={`status-badge ${emp.status === 'Active' ? 'status-active' : 'status-inactive'}`}>
                      {emp.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </motion.div>
  );
}
