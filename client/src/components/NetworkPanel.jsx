import React from 'react';
import { motion } from 'framer-motion';
import { Lock, Database, AlertTriangle } from 'lucide-react';

export default function NetworkPanel() {
  return (
    <div className="flex flex-col items-center justify-center h-full bg-gray-900 p-8">
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl w-full bg-gray-800 border border-gray-700 rounded-xl p-8 relative overflow-hidden shadow-2xl"
      >
        {/* Background grid pattern for aesthetics */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
        
        <div className="relative z-10 flex flex-col items-center text-center">
          <div className="w-16 h-16 bg-gray-900 border border-gray-700 rounded-full flex items-center justify-center mb-6">
            <Lock className="w-8 h-8 text-gray-500" />
          </div>
          
          <h2 className="text-2xl font-bold tracking-widest text-white mb-2 uppercase">Network Analysis Unavailable</h2>
          <p className="text-gray-400 mb-8 max-w-lg leading-relaxed">
            Entity-level linking and criminal network generation is currently restricted due to dataset granularity limits.
          </p>

          <div className="w-full bg-gray-900 border border-gray-700 rounded-lg p-5 text-left mb-6">
            <div className="flex items-start space-x-3">
              <Database className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
              <div>
                <h4 className="text-sm font-bold text-gray-200 mb-1 tracking-wide">SYSTEM INTEGRATION REQUIREMENT</h4>
                <p className="text-xs text-gray-400 font-mono leading-relaxed">
                  Network/link analysis requires case-level microdata (Accused IDs, Vehicle Registration, Victim IDs). Current data feeds provide statistical aggregates only.
                  <br/><br/>
                  This is a stated integration point for production deployment with SCRB's active case databases.
                </p>
              </div>
            </div>
          </div>

          <div className="w-full bg-orange-900 bg-opacity-20 border border-orange-900 rounded-lg p-4 flex items-center justify-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-orange-500" />
            <span className="text-xs font-bold text-orange-500 uppercase tracking-wider">Awaiting Microdata Feed Authorization</span>
          </div>

        </div>
      </motion.div>
    </div>
  );
}
