import React from 'react';
import { Users, AlertTriangle, Activity } from 'lucide-react';

const GangAnalysis = () => {
  return (
    <div className="flex gap-6 h-[calc(100vh-7rem)]">
      <div className="w-1/3 flex flex-col gap-6">
        <div className="glass-panel p-5 rounded-xl border-t-2 border-t-gotham-danger shadow-lg">
          <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
            <AlertTriangle className="text-gotham-danger" size={20} /> Active Communities
          </h2>
          <div className="space-y-3">
            {[
              { name: 'Downtown Syndicate', size: 24, risk: 'Critical', trend: '+12%' },
              { name: 'East Side Crew', size: 15, risk: 'High', trend: '+5%' },
              { name: 'Tech Park Scammers', size: 8, risk: 'Medium', trend: '-2%' }
            ].map((g, i) => (
              <div key={i} className={`p-4 rounded-lg border cursor-pointer transition-all ${i === 0 ? 'bg-gotham-card border-gotham-danger/50 shadow-[0_0_15px_rgba(239,68,68,0.15)]' : 'bg-gotham-bg/50 border-gotham-border hover:bg-gotham-card hover:border-gotham-border/80'}`}>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold">{g.name}</h3>
                  <span className={`text-[10px] px-2 py-1 rounded font-bold uppercase tracking-wider ${g.risk === 'Critical' ? 'bg-gotham-danger/20 text-gotham-danger' : g.risk === 'High' ? 'bg-gotham-warning/20 text-gotham-warning' : 'bg-gotham-accent/20 text-gotham-accent'}`}>
                    {g.risk}
                  </span>
                </div>
                <div className="flex justify-between text-xs text-gotham-text-sec mt-4 border-t border-gotham-border/50 pt-2">
                  <span className="flex items-center gap-1.5"><Users size={14}/> {g.size} members</span>
                  <span className="flex items-center gap-1.5"><Activity size={14}/> {g.trend} activity</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="flex-1 glass-panel p-5 rounded-xl flex flex-col shadow-lg">
          <h3 className="text-sm font-semibold mb-4 text-gotham-text-sec uppercase tracking-wider">Community Stats (Downtown Syndicate)</h3>
          <div className="space-y-4 flex-1">
            <div className="bg-gotham-card p-3 rounded-lg border border-gotham-border">
              <p className="text-xs text-gotham-text-sec mb-1">Primary Territory</p>
              <p className="font-medium text-sm">Shivajinagar, Indiranagar</p>
            </div>
            <div className="bg-gotham-card p-3 rounded-lg border border-gotham-border">
              <p className="text-xs text-gotham-text-sec mb-1">Core Activities</p>
              <p className="font-medium text-sm">Extortion, Real Estate Fraud</p>
            </div>
            <div className="bg-gotham-card p-3 rounded-lg border border-gotham-border">
              <p className="text-xs text-gotham-text-sec mb-1">Recent Escalation</p>
              <p className="font-medium text-sm text-gotham-danger flex items-center gap-2">
                <AlertTriangle size={14} /> 3 violent incidents in last 30 days
              </p>
            </div>
          </div>
          <button className="w-full bg-gotham-bg border border-gotham-border hover:bg-gotham-card hover:border-gotham-text-sec text-gotham-text py-2.5 rounded-lg text-sm transition-colors mt-4 font-medium">
            Generate Full Dossier
          </button>
        </div>
      </div>

      <div className="flex-1 glass-card rounded-xl relative overflow-hidden border border-gotham-border flex items-center justify-center">
        <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: 'radial-gradient(#3B82F6 2px, transparent 2px)', backgroundSize: '40px 40px' }}></div>
        <div className="text-center z-10 p-8 bg-gotham-bg/90 backdrop-blur-md rounded-2xl border border-gotham-border shadow-2xl max-w-md">
          <div className="w-16 h-16 bg-gotham-card rounded-full flex items-center justify-center mx-auto mb-4 border border-gotham-border">
            <Users size={32} className="text-gotham-accent" />
          </div>
          <h3 className="text-2xl font-bold mb-3">Community Graph View</h3>
          <p className="text-gotham-text-sec text-sm leading-relaxed">
            The full interactive community graph will be rendered here. 
            Nodes will be color-coded by role (Leader, Lieutenant, Soldier) and edges by relationship type.
          </p>
        </div>
      </div>
    </div>
  );
};

export default GangAnalysis;
