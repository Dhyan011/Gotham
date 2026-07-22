import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import { Info, User, Phone, CreditCard } from 'lucide-react';

const NetworkGraph = () => {
  const containerRef = useRef(null);
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    const cy = cytoscape({
      container: containerRef.current,
      elements: [
        { data: { id: 'a', label: 'Raju (Accused)', type: 'person' } },
        { data: { id: 'b', label: 'Phone: 9876543210', type: 'phone' } },
        { data: { id: 'c', label: 'Bank Acc: 1234', type: 'bank' } },
        { data: { id: 'd', label: 'Suresh (Co-accused)', type: 'person' } },
        { data: { source: 'a', target: 'b', label: 'owns' } },
        { data: { source: 'a', target: 'c', label: 'transfers' } },
        { data: { source: 'b', target: 'd', label: 'calls' } }
      ],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#3B82F6',
            'label': 'data(label)',
            'color': '#F9FAFB',
            'text-valign': 'bottom',
            'text-margin-y': 5,
            'font-size': 12,
            'border-width': 2,
            'border-color': '#2D3748'
          }
        },
        {
          selector: 'node[type="person"]',
          style: { 'background-color': '#EF4444' }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#2D3748',
            'target-arrow-color': '#2D3748',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'color': '#9CA3AF',
            'font-size': 10,
            'text-rotation': 'autorotate',
            'text-margin-y': -10
          }
        }
      ],
      layout: { name: 'cose', padding: 50 }
    });

    cy.on('tap', 'node', (evt) => {
      setSelectedNode(evt.target.data());
    });
    
    return () => cy.destroy();
  }, []);

  return (
    <div className="flex gap-4 h-[calc(100vh-7rem)] relative">
      <div className="flex-1 glass-card rounded-xl relative overflow-hidden">
        <div className="absolute top-4 left-4 z-10 w-72">
          <input type="text" placeholder="Search nodes..." className="w-full bg-gotham-bg/80 backdrop-blur border border-gotham-border rounded px-3 py-2 text-sm focus:outline-none focus:border-gotham-accent" />
        </div>
        
        <div ref={containerRef} className="w-full h-full" />
        
        <div className="absolute bottom-4 left-4 bg-gotham-bg/90 backdrop-blur p-3 rounded-lg border border-gotham-border z-10 text-xs flex flex-col gap-2 shadow-lg">
          <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-gotham-danger"></div> Person</div>
          <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-gotham-accent"></div> Asset / Device</div>
        </div>
      </div>
      
      {selectedNode ? (
        <div className="w-80 glass-panel p-4 rounded-xl flex flex-col transform transition-transform duration-300">
          <div className="flex justify-between items-center mb-4 border-b border-gotham-border pb-3">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              {selectedNode.type === 'person' ? <User size={18} className="text-gotham-danger"/> : <Phone size={18} className="text-gotham-accent"/>}
              {selectedNode.label}
            </h3>
            <button onClick={() => setSelectedNode(null)} className="text-gotham-text-sec hover:text-white bg-gotham-card rounded p-1">✕</button>
          </div>
          <div className="space-y-3 text-sm flex-1 overflow-y-auto">
            <div className="bg-gotham-card/50 p-3 rounded-lg border border-gotham-border/50">
              <p className="text-gotham-text-sec mb-1 text-xs uppercase tracking-wider">Entity Type</p>
              <p className="capitalize font-medium">{selectedNode.type}</p>
            </div>
            <div className="bg-gotham-card/50 p-3 rounded-lg border border-gotham-border/50">
              <p className="text-gotham-text-sec mb-1 text-xs uppercase tracking-wider">Risk Level</p>
              <p className="text-gotham-danger font-bold">High</p>
            </div>
            <div className="bg-gotham-card/50 p-3 rounded-lg border border-gotham-border/50">
              <p className="text-gotham-text-sec mb-2 text-xs uppercase tracking-wider">Associated Cases</p>
              <div className="flex gap-2">
                <span className="bg-gotham-bg px-2 py-1 rounded text-xs border border-gotham-border">CAS-101</span>
                <span className="bg-gotham-bg px-2 py-1 rounded text-xs border border-gotham-border">CAS-105</span>
              </div>
            </div>
          </div>
          <button className="w-full mt-4 bg-gotham-accent hover:bg-blue-600 text-white py-2 rounded transition-colors text-sm font-medium">
            Expand Network
          </button>
        </div>
      ) : (
        <div className="w-80 glass-panel p-4 rounded-xl flex items-center justify-center text-gotham-text-sec text-sm text-center">
          Select a node on the canvas to view detailed intelligence.
        </div>
      )}
    </div>
  );
};

export default NetworkGraph;
