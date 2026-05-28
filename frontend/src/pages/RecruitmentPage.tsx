import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Briefcase, MapPin, DollarSign, Users } from 'lucide-react';

interface JobPosting {
  id: string;
  title: string;
  department: string;
  location: string;
  salary_range: string;
  status: string;
  posted_date: string;
  applicants: number;
  description: string;
}

export default function RecruitmentPage() {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/recruitment/jobs')
      .then(res => res.json())
      .then(data => {
        setJobs(data);
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
        <div className="page-header__icon" style={{ color: '#6366f1', backgroundColor: 'rgba(99, 102, 241, 0.1)' }}>
          <Briefcase size={24} />
        </div>
        <div>
          <h1 className="page-title">Recruitment Dashboard</h1>
          <p className="page-subtitle">Manage open requisitions and job postings</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="grid-cards">
          {jobs.map(job => (
            <div key={job.id} className="card">
              <div className="card-header">
                <h3 className="card-title">{job.title}</h3>
                <span className={`status-badge ${job.status === 'Open' ? 'status-active' : 'status-inactive'}`}>
                  {job.status}
                </span>
              </div>
              <p className="card-text">{job.department}</p>
              <div className="card-details">
                <span className="card-detail-item"><MapPin size={14}/> {job.location}</span>
                <span className="card-detail-item"><DollarSign size={14}/> {job.salary_range}</span>
                <span className="card-detail-item"><Users size={14}/> {job.applicants} Applicants</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
