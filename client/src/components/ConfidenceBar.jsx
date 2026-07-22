import React from 'react';

const ConfidenceBar = ({ value }) => {
  const percentage = Math.round(value * 100);
  
  let colorClass = 'from-gotham-success to-emerald-400';
  if (value < 0.5) colorClass = 'from-gotham-danger to-red-400';
  else if (value < 0.8) colorClass = 'from-gotham-warning to-yellow-400';

  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-gotham-bg rounded-full overflow-hidden border border-gotham-border">
        <div 
          className={`h-full rounded-full bg-gradient-to-r ${colorClass} transition-all duration-1000 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-xs font-mono text-gotham-text-sec w-8">{percentage}%</span>
    </div>
  );
};

export default ConfidenceBar;
