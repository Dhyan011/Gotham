import React from 'react';
import Timeline from './Timeline';
import { ShieldAlert, User, FileText, CheckCircle2 } from 'lucide-react';

export default function CaseView({ caseData, riskScore }) {
  if (!caseData) return <div className="p-4 text-gray-500">No active case selected.</div>;

  return (
    <div className="flex flex-col h-full bg-[#0a0a0a] border border-gray-800 rounded-xl overflow-hidden p-6 overflow-y-auto">
      
      {/* Header */}
      <div className="flex items-center justify-between mb-6 border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-100 flex items-center gap-2">
            <ShieldAlert className="text-red-500" />
            {caseData.title}
          </h1>
          <p className="text-sm text-gray-400 mt-1 font-mono">Case ID: {caseData.id} | Primary: {caseData.primary_fir}</p>
        </div>
        <div className="text-right">
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-green-900/30 text-green-400 text-xs font-medium border border-green-800/50">
            <CheckCircle2 className="w-3 h-3" />
            STATUS: {caseData.status}
          </span>
          <p className="text-xs text-gray-500 mt-2">Officer: {caseData.assigned_officer}</p>
        </div>
      </div>

      {/* AI Summary */}
      <div className="bg-blue-900/10 border border-blue-900/50 rounded-lg p-4 mb-6">
        <h3 className="text-xs font-semibold text-blue-400 uppercase tracking-widest mb-2 flex items-center gap-2">
          <FileText className="w-4 h-4" /> AI Intelligence Summary
        </h3>
        <p className="text-sm text-blue-100/80 leading-relaxed">
          {caseData.ai_summary}
        </p>
      </div>

      {/* Risk Target (If retrieved by Copilot) */}
      {riskScore && (
        <div className="bg-red-900/10 border border-red-900/50 rounded-lg p-4 mb-6">
          <h3 className="text-xs font-semibold text-red-400 uppercase tracking-widest mb-2 flex items-center gap-2">
            <User className="w-4 h-4" /> Primary Target Risk Score
          </h3>
          <div className="flex items-end gap-4">
            <div className="text-4xl font-black text-red-500">{riskScore.score}</div>
            <div className="pb-1">
              <span className="text-xs px-2 py-1 bg-red-900/30 text-red-300 rounded font-mono">Confidence: {riskScore.confidence}</span>
              <p className="text-sm text-red-200/80 mt-2">{riskScore.reasoning}</p>
            </div>
          </div>
        </div>
      )}

      {/* Timeline */}
      <div className="mt-auto">
        <Timeline events={caseData.timeline_events} />
      </div>

    </div>
  );
}
