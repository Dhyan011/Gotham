import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import CountUp from 'react-countup';
import { AlertOctagon, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export default function AnomalyDashboard() {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const API_BASE = import.meta.env.VITE_API_URL || '/server/backend_service';
    axios.get(`${API_BASE}/api/stats/anomalies`)
      .then(res => {
        if (res.data.status === 'success') {
          setAnomalies(res.data.anomalies);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching anomalies:", err);
        setLoading(false);
      });
  }, []);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
  };

  const renderTrendIcon = (trend) => {
    if (trend === "UPWARD") return <TrendingUp className="w-4 h-4 text-red-400" />;
    if (trend === "DOWNWARD") return <TrendingDown className="w-4 h-4 text-green-400" />;
    return <Minus className="w-4 h-4 text-gray-500" />;
  };

  return (
    <div className="flex flex-col h-full bg-gray-950 text-gray-200 p-8 overflow-y-auto">
      
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-2xl font-bold tracking-widest text-cyan-500 mb-2 flex items-center">
          <AlertOctagon className="w-6 h-6 mr-3 opacity-80" />
          STATISTICAL ANOMALY DETECTION
        </h1>
        <p className="text-sm font-mono text-gray-500 uppercase tracking-widest">
          Pattern recognition heuristics applied to monthly aggregates
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {[1, 2, 3, 4].map(n => (
            <div key={n} className="bg-gray-900 border border-gray-800 rounded p-6 h-48 animate-pulse">
              <div className="h-6 bg-gray-800 rounded w-1/2 mb-6"></div>
              <div className="flex space-x-4 mb-4">
                <div className="h-10 bg-gray-800 rounded w-16"></div>
                <div className="h-10 bg-gray-800 rounded w-16"></div>
              </div>
              <div className="h-4 bg-gray-800 rounded w-full mt-auto"></div>
            </div>
          ))}
        </div>
      ) : anomalies.length === 0 ? (
        <div className="bg-gray-900 p-12 rounded border border-gray-800 text-center max-w-2xl mx-auto mt-12">
          <p className="text-gray-400 font-mono text-sm">SYSTEM NOMINAL. NO STATISTICAL DEVIATIONS DETECTED IN CURRENT WINDOW.</p>
        </div>
      ) : (
        <motion.div 
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
        >
          {anomalies.map((anomaly, idx) => (
            <motion.div 
              variants={item}
              key={idx} 
              className={`bg-gray-900 rounded p-5 relative overflow-hidden flex flex-col ${
                anomaly.severity === 'HIGH' ? 'border border-red-500 pulse-border-red shadow-[0_0_15px_rgba(239,68,68,0.15)]' : 
                anomaly.severity === 'MEDIUM' ? 'border border-orange-500' : 'border border-gray-700'
              }`}
            >
              <div className="flex justify-between items-start mb-6 z-10">
                <h3 className="text-sm font-bold text-gray-100 max-w-[70%] leading-snug">{anomaly.crime_type}</h3>
                <span className={`px-2 py-1 text-[10px] font-mono font-bold tracking-widest rounded uppercase ${
                  anomaly.severity === 'HIGH' ? 'bg-red-500 text-black' : 
                  anomaly.severity === 'MEDIUM' ? 'bg-orange-500 text-black' : 'bg-gray-700 text-gray-300'
                }`}>
                  {anomaly.severity}
                </span>
              </div>
              
              <div className="flex items-center space-x-8 mb-6 z-10">
                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Current</p>
                  <p className="text-3xl font-mono text-white">
                    <CountUp end={anomaly.current} duration={1.5} />
                  </p>
                </div>
                <div className="h-8 w-px bg-gray-800"></div>
                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Previous</p>
                  <p className="text-2xl font-mono text-gray-400">
                    <CountUp end={anomaly.previous} duration={1.5} />
                  </p>
                </div>
                
                {/* Phase 5 Trend Indicator */}
                <div className="ml-auto bg-gray-950 p-2 rounded flex items-center space-x-2 border border-gray-800">
                  {renderTrendIcon(anomaly.trend)}
                  <span className="text-[10px] font-mono text-gray-400">{anomaly.trend}</span>
                </div>
              </div>

              {/* Phase 6 Confidence / Basis Block */}
              <div className="mt-auto bg-black bg-opacity-40 p-3 rounded border border-gray-800 z-10">
                <p className="text-[10px] uppercase tracking-widest text-gray-600 mb-1">Confidence Basis</p>
                <p className="text-xs text-cyan-500 font-mono opacity-80 leading-relaxed">
                  {anomaly.basis}
                </p>
              </div>
              
              {/* Background accent based on severity */}
              {anomaly.severity === 'HIGH' && (
                <div className="absolute top-0 right-0 w-32 h-32 bg-red-500 opacity-[0.03] rounded-full blur-3xl transform translate-x-10 -translate-y-10"></div>
              )}
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
