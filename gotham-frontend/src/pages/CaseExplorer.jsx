import React, { useState } from 'react';
import { mockCases, mockRecentFirs } from '../utils/mockData';
import { Search, Filter, ChevronRight } from 'lucide-react';

const CaseExplorer = () => {
  const [selectedCase, setSelectedCase] = useState(mockCases[0]);

  return (
    <div className="flex gap-4 h-[calc(100vh-7rem)]">
      <div className="w-80 flex flex-col gap-4">
        <div className="glass-panel p-4 rounded-xl flex flex-col gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gotham-text-sec" size={16} />
            <input type="text" placeholder="Search cases..." className="w-full bg-gotham-bg border border-gotham-border rounded py-1.5 pl-9 pr-3 text-sm focus:outline-none focus:border-gotham-accent text-gotham-text placeholder:text-gotham-text-sec" />
          </div>
          <div className="flex gap-2">
            <button className="flex-1 bg-gotham-card border border-gotham-border rounded py-1.5 text-xs text-gotham-text-sec flex items-center justify-center gap-1 hover:text-white hover:border-gotham-text-sec transition-colors">
              <Filter size={12}/> Status
            </button>
            <button className="flex-1 bg-gotham-card border border-gotham-border rounded py-1.5 text-xs text-gotham-text-sec flex items-center justify-center gap-1 hover:text-white hover:border-gotham-text-sec transition-colors">
              <Filter size={12}/> District
            </button>
          </div>
        </div>
        
        <div className="flex-1 glass-panel rounded-xl overflow-y-auto p-2 space-y-2">
          {mockCases.concat(mockCases).map((c, i) => (
            <div 
              key={i} 
              onClick={() => setSelectedCase(c)}
              className={`p-3 rounded-lg cursor-pointer transition-all border ${selectedCase.id === c.id ? 'bg-gotham-card border-gotham-accent shadow-[0_0_10px_rgba(59,130,246,0.15)]' : 'border-transparent hover:bg-gotham-card hover:border-gotham-border'}`}
            >
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs font-mono text-gotham-accent">{c.id}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded border font-medium ${c.risk === 'High' ? 'bg-gotham-danger/10 border-gotham-danger/30 text-gotham-danger' : 'bg-gotham-warning/10 border-gotham-warning/30 text-gotham-warning'}`}>{c.risk} Risk</span>
              </div>
              <h4 className="font-medium text-sm text-gotham-text mb-1">{c.title}</h4>
              <p className="text-xs text-gotham-text-sec">{c.status}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="flex-1 glass-card rounded-xl p-6 overflow-y-auto">
        {selectedCase ? (
          <div className="space-y-6">
            <div className="flex justify-between items-start border-b border-gotham-border pb-4">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-2xl font-bold">{selectedCase.title}</h2>
                  <span className="px-2 py-1 bg-gotham-card border border-gotham-border rounded text-xs text-gotham-text-sec font-mono">{selectedCase.id}</span>
                </div>
                <p className="text-sm text-gotham-text-sec">Initiated: Oct 2023 | Assigned to: IO Ramesh</p>
              </div>
              <button className="bg-gotham-accent hover:bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium transition-colors shadow-[0_0_15px_rgba(59,130,246,0.4)]">
                Generate Report
              </button>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="font-semibold text-sm border-b border-gotham-border pb-2">Primary Suspects</h3>
                <div className="bg-gotham-bg/50 p-3 rounded-lg border border-gotham-border flex items-center justify-between hover:bg-gotham-card transition-colors cursor-pointer">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded bg-gotham-danger/20 border border-gotham-danger/40 flex items-center justify-center text-gotham-danger font-bold text-lg">R</div>
                    <div>
                      <p className="font-medium text-sm">Raju Kumar</p>
                      <p className="text-xs text-gotham-text-sec">Role: Mastermind</p>
                    </div>
                  </div>
                  <ChevronRight size={16} className="text-gotham-text-sec" />
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-sm border-b border-gotham-border pb-2">Similar Historical Cases</h3>
                <div className="bg-gotham-bg/50 p-3 rounded-lg border border-gotham-border">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gotham-accent font-mono">CAS-045</span>
                    <span className="text-gotham-success text-xs font-bold bg-gotham-success/10 px-2 py-0.5 rounded">92% Match</span>
                  </div>
                  <p className="text-xs text-gotham-text-sec">Extortion ring busted in 2021 with identical MO.</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold text-sm border-b border-gotham-border pb-2 mb-4">Case Timeline</h3>
              <div className="space-y-4 pl-2 border-l-2 border-gotham-border ml-2">
                <div className="relative pl-6">
                  <div className="absolute w-3 h-3 bg-gotham-accent rounded-full -left-[27px] top-1 border-2 border-gotham-bg"></div>
                  <p className="text-xs text-gotham-text-sec mb-1 font-mono">Oct 25, 2023</p>
                  <p className="text-sm bg-gotham-card p-3 rounded-lg border border-gotham-border inline-block shadow-sm">FIR Filed by victim in Indiranagar PS</p>
                </div>
                <div className="relative pl-6">
                  <div className="absolute w-3 h-3 bg-gotham-warning rounded-full -left-[27px] top-1 border-2 border-gotham-bg"></div>
                  <p className="text-xs text-gotham-text-sec mb-1 font-mono">Oct 26, 2023</p>
                  <p className="text-sm bg-gotham-card p-3 rounded-lg border border-gotham-border inline-block shadow-sm">CCTV footage recovered showing suspect vehicle</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gotham-text-sec">
            Select a case to view details
          </div>
        )}
      </div>
    </div>
  );
};

export default CaseExplorer;
