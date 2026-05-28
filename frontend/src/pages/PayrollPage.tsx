import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { DollarSign, FileText } from 'lucide-react';

interface Payslip {
  employee_id: string;
  employee_name: string;
  pay_period: string;
  gross_salary: number;
  net_pay: number;
  payment_date: string;
  payment_method: string;
}

export default function PayrollPage() {
  const [payslips, setPayslips] = useState<Payslip[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/payroll/')
      .then(res => res.json())
      .then(data => {
        setPayslips(data);
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
        <div className="page-header__icon" style={{ color: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)' }}>
          <DollarSign size={24} />
        </div>
        <div>
          <h1 className="page-title">Payroll</h1>
          <p className="page-subtitle">Compensation and payslip distribution</p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading...</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Employee</th>
                <th>Period</th>
                <th>Payment Date</th>
                <th>Method</th>
                <th>Gross Salary</th>
                <th>Net Pay</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {payslips.map((ps, i) => (
                <tr key={i}>
                  <td>
                    <div className="font-medium">{ps.employee_name}</div>
                    <div className="text-xs text-slate-400">{ps.employee_id}</div>
                  </td>
                  <td>{ps.pay_period}</td>
                  <td>{ps.payment_date}</td>
                  <td>{ps.payment_method}</td>
                  <td>${ps.gross_salary.toLocaleString()}</td>
                  <td className="text-emerald-400 font-medium">${ps.net_pay.toLocaleString()}</td>
                  <td>
                    <button className="flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300">
                      <FileText size={14} /> View
                    </button>
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
