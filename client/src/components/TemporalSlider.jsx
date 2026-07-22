import React from 'react';

const TemporalSlider = () => {
  return (
    <div className="bg-gotham-card p-4 rounded-lg border border-gotham-border w-full">
      <div className="flex justify-between text-xs text-gotham-text-sec mb-2 font-mono">
        <span>2020</span>
        <span>2021</span>
        <span>2022</span>
        <span>2023</span>
      </div>
      <input 
        type="range" 
        min="2020" 
        max="2023" 
        defaultValue="2023"
        className="w-full h-1 bg-gotham-bg rounded-lg appearance-none cursor-pointer accent-gotham-accent"
      />
    </div>
  );
};

export default TemporalSlider;
