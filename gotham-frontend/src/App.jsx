import React, { useState } from 'react';
import CaseView from './components/CaseView';
import ForceGraph from './components/ForceGraph';
import Copilot from './components/Copilot';
import { api } from './utils/api';
import { Shield } from 'lucide-react';

export default function App() {
  const [caseData, setCaseData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [riskScore, setRiskScore] = useState(null);

  // Triggered when the Copilot finishes its animation sequence
  const handleCopilotComplete = async () => {
    try {
      // 1. Load Case Data
      const caseRes = await api.getCase(1);
      setCaseData(caseRes);
      
      // 2. Load the Ontology Subgraph
      const graphRes = await api.getGraphNeighbors("Ravi Kumar");
      setGraphData(graphRes);
      
      // 3. Load the Target Risk Score
      const riskRes = await api.getRiskScore("Ravi Kumar");
      setRiskScore(riskRes);
      
    } catch (err) {
      console.error("Failed to load investigation data", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#000] text-gray-200 font-sans p-4 flex flex-col">
      
      {/* Topbar */}
      <header className="flex items-center gap-3 mb-4 px-2">
        <Shield className="w-8 h-8 text-blue-500" />
        <h1 className="text-xl font-bold tracking-widest text-gray-100 uppercase">
          GOTHAM <span className="text-blue-500 font-light">Intelligence OS</span>
        </h1>
      </header>

      {/* Main Workspace Layout */}
      <div className="flex-1 grid grid-cols-12 gap-4 overflow-hidden">
        
        {/* Left Panel: Copilot (3 cols) */}
        <div className="col-span-3 flex flex-col h-full">
          <Copilot onCopilotComplete={handleCopilotComplete} />
        </div>

        {/* Center Panel: Case Workspace (5 cols) */}
        <div className="col-span-5 flex flex-col h-full">
          <CaseView caseData={caseData} riskScore={riskScore} />
        </div>

        {/* Right Panel: Ontology Graph (4 cols) */}
        <div className="col-span-4 flex flex-col h-full bg-[#0a0a0a] border border-gray-800 rounded-xl overflow-hidden p-2">
           <h3 className="text-xs font-semibold text-gray-400 mb-2 pl-2 tracking-wider uppercase">Ontology Network</h3>
           <div className="flex-1 rounded-lg overflow-hidden">
             <ForceGraph graphData={graphData} />
           </div>
        </div>

      </div>
    </div>
  );
}
