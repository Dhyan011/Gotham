import React, { useState } from 'react';
import { api } from '../utils/api';
import { Terminal, Send, Loader2, CheckCircle2 } from 'lucide-react';

export default function Copilot({ onCopilotComplete }) {
  const [command, setCommand] = useState("");
  const [steps, setSteps] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  const handleInvestigate = async () => {
    if (!command.includes("1245")) {
      alert("Demo Mode: Please use command 'Investigate FIR 1245'");
      return;
    }

    setIsRunning(true);
    setSteps([]);
    
    try {
      const data = await api.triggerCopilot(command);
      const pipeline = data.pipeline;
      
      // Animate steps sequentially
      for (let i = 0; i < pipeline.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1200)); // 1.2s delay per step
        setSteps(prev => [...prev, pipeline[i]]);
      }
      
      onCopilotComplete(); // Trigger parent to load graph and risk score
    } catch (err) {
      console.error(err);
      alert("Copilot Error: Is the backend running?");
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0a0a0a] border border-gray-800 rounded-xl overflow-hidden">
      
      <div className="p-4 bg-[#111] border-b border-gray-800 flex items-center gap-2">
        <Terminal className="text-purple-500 w-5 h-5" />
        <h2 className="text-gray-100 font-semibold tracking-wide uppercase text-sm">Investigation Copilot</h2>
      </div>

      <div className="flex-1 p-4 overflow-y-auto font-mono text-sm space-y-4">
        {steps.map((s, i) => (
          <div key={i} className="animate-fade-in-up">
            <div className="text-purple-400 font-bold mb-1">[{s.action}]</div>
            <div className="text-gray-400 pl-2 border-l-2 border-gray-700">{s.message}</div>
            <div className="text-green-400 pl-2 mt-1 flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />
              <span>{s.result}</span>
            </div>
          </div>
        ))}
        {isRunning && (
          <div className="flex items-center gap-2 text-gray-500 mt-4">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Orchestrating AI Pipeline...</span>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-800 bg-[#111]">
        <div className="flex items-center gap-2 bg-[#000] border border-gray-700 rounded-lg p-1 focus-within:border-purple-500 transition-colors">
          <input 
            className="flex-1 bg-transparent text-gray-100 p-2 outline-none placeholder-gray-600 font-mono text-sm"
            placeholder="e.g. Investigate FIR 1245"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleInvestigate()}
            disabled={isRunning}
          />
          <button 
            onClick={handleInvestigate}
            disabled={isRunning || !command}
            className="p-2 bg-purple-600 hover:bg-purple-500 text-white rounded disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

    </div>
  );
}
