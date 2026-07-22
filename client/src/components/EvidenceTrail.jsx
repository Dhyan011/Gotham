import React from 'react';
import { X, ArrowRight, ShieldCheck } from 'lucide-react';

const EvidenceTrail = ({ isOpen, onClose, trail }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gotham-bg-sec border border-gotham-border rounded-xl w-full max-w-2xl shadow-2xl glass-card flex flex-col">
        <div className="p-4 border-b border-gotham-border flex justify-between items-center">
          <h3 className="font-semibold flex items-center gap-2">
            <ShieldCheck className="text-gotham-accent" size={18} />
            Inference Evidence Trail
          </h3>
          <button onClick={onClose} className="text-gotham-text-sec hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto max-h-[60vh] space-y-4">
          {(trail || ['Call records mapped to tower', 'Social media association found', 'Financial transaction verified']).map((step, idx) => (
            <div key={idx} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-6 h-6 rounded-full bg-gotham-bg border border-gotham-accent flex items-center justify-center text-xs text-gotham-accent font-bold">
                  {idx + 1}
                </div>
                {idx !== (trail?.length || 3) - 1 && (
                  <div className="w-px h-full bg-gotham-border my-1" />
                )}
              </div>
              <div className="bg-gotham-card p-3 rounded-lg border border-gotham-border flex-1 mb-2">
                <p className="text-sm">{step}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EvidenceTrail;
