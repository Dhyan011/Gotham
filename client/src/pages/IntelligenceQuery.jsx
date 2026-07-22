import React, { useState } from 'react';
import ConfidenceBar from '../components/ConfidenceBar';
import EvidenceTrail from '../components/EvidenceTrail';
import { Search, ChevronRight } from 'lucide-react';

const IntelligenceQuery = () => {
  const [showTrail, setShowTrail] = useState(false);

  return (
    <div className="flex gap-6 h-[calc(100vh-7rem)] max-w-7xl mx-auto">
      <div className="w-1/3 glass-panel p-6 rounded-xl flex flex-col gap-6">
        <div>
          <h2 className="text-xl font-bold mb-1">Intelligence Query</h2>
          <p className="text-xs text-gotham-text-sec">Enter known parameters to find matches.</p>
        </div>

        <form className="space-y-4 flex-1 overflow-y-auto pr-2">
          {[
            { label: 'Name / Alias', type: 'text', placeholder: 'e.g. Raju, Ghost' },
            { label: 'Physical Description', type: 'text', placeholder: 'e.g. Scar on left cheek' },
            { label: 'Vehicle Details', type: 'text', placeholder: 'e.g. Black SUV, KA-01' },
            { label: 'Location Area', type: 'text', placeholder: 'e.g. Indiranagar' },
            { label: 'Date Range', type: 'text', placeholder: 'Select dates' },
            { label: 'Crime Type', type: 'text', placeholder: 'e.g. Extortion' },
          ].map((field, i) => (
            <div key={i}>
              <label className="block text-xs font-semibold text-gotham-text-sec mb-1.5 uppercase">{field.label}</label>
              <input 
                type={field.type} 
                placeholder={field.placeholder}
                className="w-full bg-gotham-bg border border-gotham-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-gotham-accent transition-colors text-gotham-text placeholder:text-gotham-text-sec/50"
              />
            </div>
          ))}
        </form>

        <button className="w-full bg-gotham-accent hover:bg-blue-600 text-white py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2 shadow-[0_0_15px_rgba(59,130,246,0.3)]">
          <Search size={18} /> Run Analysis
        </button>
      </div>

      <div className="flex-1 glass-card rounded-xl p-6 flex flex-col border border-gotham-border">
        <h3 className="font-semibold text-lg mb-6 border-b border-gotham-border pb-4">Ranked Candidates</h3>
        
        <div className="space-y-4 overflow-y-auto flex-1 pr-2">
          {[
            { name: 'Raju Kumar', alias: 'Ghost', conf: 0.92, matches: ['Location', 'Crime Type', 'Alias'] },
            { name: 'Suresh M.', alias: 'Surya', conf: 0.65, matches: ['Location', 'Crime Type'] },
            { name: 'Unknown', alias: 'N/A', conf: 0.35, matches: ['Vehicle Type'] },
          ].map((cand, i) => (
            <div key={i} className="bg-gotham-bg/60 p-5 rounded-xl border border-gotham-border/50 hover:border-gotham-accent/30 transition-all hover:bg-gotham-card group cursor-pointer relative overflow-hidden">
              {i === 0 && <div className="absolute top-0 left-0 w-1 h-full bg-gotham-success shadow-[0_0_10px_currentColor]"></div>}
              <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gotham-bg flex items-center justify-center text-gotham-text-sec border border-gotham-border font-bold">
                    {cand.name.charAt(0)}
                  </div>
                  <div>
                    <h4 className="font-semibold text-lg flex items-center gap-2">
                      {cand.name} <span className="text-xs bg-gotham-card px-2 py-0.5 rounded text-gotham-text-sec font-normal border border-gotham-border">'{cand.alias}'</span>
                    </h4>
                  </div>
                </div>
                <button 
                  onClick={() => setShowTrail(true)}
                  className="text-xs text-gotham-accent hover:text-white flex items-center gap-1 bg-gotham-accent/10 px-3 py-1.5 rounded-full border border-gotham-accent/20 transition-colors"
                >
                  View Evidence <ChevronRight size={14}/>
                </button>
              </div>
              
              <div className="mb-4">
                <div className="flex justify-between text-xs mb-1 text-gotham-text-sec">
                  <span>Match Confidence</span>
                </div>
                <ConfidenceBar value={cand.conf} />
              </div>

              <div>
                <p className="text-xs text-gotham-text-sec mb-2">Matched Parameters:</p>
                <div className="flex gap-2">
                  {cand.matches.map((m, j) => (
                    <span key={j} className="text-[10px] bg-gotham-bg px-2 py-1 rounded border border-gotham-border text-gotham-text-sec">
                      {m}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <EvidenceTrail isOpen={showTrail} onClose={() => setShowTrail(false)} />
    </div>
  );
};

export default IntelligenceQuery;
