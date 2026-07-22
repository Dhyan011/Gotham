import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { mockAlerts } from '../utils/mockData';

const AlertBanner = () => {
  return (
    <div className="w-full bg-gotham-danger/10 border border-gotham-danger/30 rounded-lg p-3 mb-4 flex items-center gap-3 glass-panel">
      <AlertTriangle className="text-gotham-danger animate-pulse" size={20} />
      <div className="flex-1 overflow-hidden relative h-6">
        <div className="absolute whitespace-nowrap text-sm text-gotham-text animate-[marquee_15s_linear_infinite]">
          {mockAlerts.map(alert => (
            <span key={alert.id} className="mr-8">
              <span className="bg-gotham-danger text-white text-[10px] px-2 py-0.5 rounded font-bold uppercase mr-2">
                {alert.severity}
              </span>
              {alert.text}
            </span>
          ))}
        </div>
      </div>
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(100%); }
          100% { transform: translateX(-100%); }
        }
      `}</style>
    </div>
  );
};

export default AlertBanner;
