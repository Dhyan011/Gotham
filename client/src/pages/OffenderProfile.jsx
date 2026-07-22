import React from 'react';
import { mockOffender } from '../utils/mockData';
import { Activity, FileText, Tag, Users } from 'lucide-react';

const OffenderProfile = () => {
  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-8">
      <div className="glass-card rounded-2xl p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-gotham-danger/20 rounded-full blur-[80px] -mr-20 -mt-20"></div>
        <div className="flex gap-8 relative z-10 items-center">
          <div className="w-32 h-32 bg-gotham-bg/50 backdrop-blur border-2 border-gotham-danger/50 rounded-2xl flex items-center justify-center text-5xl text-gotham-danger font-bold shadow-[0_0_30px_rgba(239,68,68,0.2)]">
            {mockOffender.name.charAt(0)}
          </div>
          <div className="flex-1 flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold mb-2 tracking-tight">{mockOffender.name}</h1>
              <p className="text-gotham-text-sec mb-4 text-sm">Last Known Location: <span className="text-gotham-text">{mockOffender.lastKnown}</span></p>
              <div className="flex gap-2">
                {mockOffender.tags.map((tag, i) => (
                  <span key={i} className="bg-gotham-danger/10 border border-gotham-danger/30 text-gotham-danger px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                    <Tag size={12}/> {tag}
                  </span>
                ))}
              </div>
            </div>
            <div className="text-center mr-8">
              <div className="w-28 h-28 rounded-full border-[6px] border-gotham-bg flex items-center justify-center flex-col shadow-[0_0_0_4px_rgba(239,68,68,0.5)] relative">
                <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="46" fill="none" stroke="#2D3748" strokeWidth="8" />
                  <circle cx="50" cy="50" r="46" fill="none" stroke="#EF4444" strokeWidth="8" strokeDasharray={`${mockOffender.riskScore * 2.89} 289`} strokeLinecap="round" />
                </svg>
                <span className="text-3xl font-bold text-gotham-text z-10">{mockOffender.riskScore}</span>
                <span className="text-[10px] text-gotham-text-sec uppercase tracking-widest z-10 mt-1">Risk</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 space-y-6">
          <div className="glass-panel p-6 rounded-xl">
            <h3 className="font-semibold mb-6 flex items-center gap-2 text-lg"><Activity size={20} className="text-gotham-accent"/> Modus Operandi & Risk Breakdown</h3>
            <div className="space-y-5">
              {[
                { label: 'Violence Tendency', val: 85, color: 'bg-gotham-danger' },
                { label: 'Flight Risk', val: 90, color: 'bg-gotham-warning' },
                { label: 'Network Influence', val: 75, color: 'bg-gotham-accent' }
              ].map((r, i) => (
                <div key={i}>
                  <div className="flex justify-between text-xs mb-2 font-medium">
                    <span>{r.label}</span>
                    <span className="text-gotham-text-sec">{r.val}%</span>
                  </div>
                  <div className="w-full bg-gotham-bg h-2 rounded-full overflow-hidden border border-gotham-border">
                    <div className={`h-full ${r.color} shadow-[0_0_10px_currentColor]`} style={{ width: `${r.val}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel p-6 rounded-xl">
            <h3 className="font-semibold mb-6 flex items-center gap-2 text-lg"><FileText size={20} className="text-gotham-accent"/> Case History ({mockOffender.cases})</h3>
            <div className="space-y-0 pl-3">
              {[2023, 2021, 2019].map((year, i) => (
                <div key={year} className="flex gap-5 relative">
                  <div className="flex flex-col items-center">
                    <div className="w-4 h-4 bg-gotham-bg rounded-full border-2 border-gotham-accent z-10"></div>
                    {i !== 2 && <div className="w-0.5 h-full bg-gotham-border -my-1 absolute top-4 bottom-0"></div>}
                  </div>
                  <div className="pb-8 flex-1">
                    <span className="text-xs font-bold text-gotham-accent tracking-widest">{year}</span>
                    <div className="bg-gotham-card p-4 rounded-lg mt-2 border border-gotham-border/50 shadow-sm hover:border-gotham-accent/30 transition-colors">
                      <p className="text-sm font-semibold mb-1">Armed Robbery - Indiranagar PS</p>
                      <p className="text-xs text-gotham-text-sec">Convicted, served 2 years. Associated with local gang activity.</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-xl">
            <h3 className="font-semibold mb-5 flex items-center gap-2 text-lg"><Users size={20} className="text-gotham-accent"/> Known Associates</h3>
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="flex items-center gap-4 bg-gotham-card/50 p-3 rounded-lg border border-gotham-border/50 hover:bg-gotham-card transition-colors cursor-pointer">
                  <div className="w-10 h-10 bg-gotham-bg rounded-full flex items-center justify-center text-sm font-bold border border-gotham-danger/30 text-gotham-danger">S</div>
                  <div>
                    <p className="text-sm font-medium">Suresh M.</p>
                    <p className="text-[10px] text-gotham-text-sec mt-0.5 bg-gotham-bg inline-block px-1.5 py-0.5 rounded border border-gotham-border">Co-accused CAS-101</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OffenderProfile;
