import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Clock, Award } from 'lucide-react';

interface Program {
  id: string;
  title: string;
  category: string;
  format: string;
  duration: string;
  provider: string;
  status: string;
  description: string;
  enrolled: number;
  capacity: number;
}

export default function TrainingPage() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/training/')
      .then(res => res.json())
      .then(data => {
        setPrograms(data);
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
        <div className="page-header__icon" style={{ color: '#14b8a6', backgroundColor: 'rgba(20, 184, 166, 0.1)' }}>
          <BookOpen size={24} />
        </div>
        <div>
          <h1 className="page-title">Training & Development</h1>
          <p className="page-subtitle">Course catalog and skills development</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="grid-cards">
          {programs.map(prog => (
            <div key={prog.id} className="card">
              <div className="card-header">
                <h3 className="card-title text-teal-400">{prog.title}</h3>
                <span className={`status-badge ${prog.status === 'Mandatory' ? 'bg-red-500/10 text-red-500' : 'bg-teal-500/10 text-teal-500'}`}>
                  {prog.status}
                </span>
              </div>
              <p className="card-text mb-4 line-clamp-2">{prog.description}</p>
              
              <div className="flex flex-col gap-2 text-sm text-slate-300 border-t border-slate-800 pt-3">
                <div className="flex justify-between">
                  <span className="flex items-center gap-1"><Award size={14}/> {prog.category}</span>
                  <span className="flex items-center gap-1"><Clock size={14}/> {prog.duration}</span>
                </div>
                <div className="flex justify-between mt-1 text-slate-400">
                  <span>{prog.format} • {prog.provider}</span>
                  <span>{prog.enrolled}/{prog.capacity} Enrolled</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
