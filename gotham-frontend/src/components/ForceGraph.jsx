import React, { useRef, useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

export default function ForceGraph({ graphData }) {
  const fgRef = useRef();

  useEffect(() => {
    // Make the graph fit to bounds once data loads
    if (graphData && graphData.nodes.length && fgRef.current) {
      setTimeout(() => {
        fgRef.current.zoomToFit(400, 50);
      }, 500);
    }
  }, [graphData]);

  if (!graphData || !graphData.nodes) return <div className="p-4 text-gray-400">Loading Ontology Graph...</div>;

  return (
    <div className="w-full h-full bg-[#0a0a0a] rounded-xl overflow-hidden border border-gray-800">
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        nodeLabel="label"
        nodeAutoColorBy="group"
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowRelPos={1}
        linkCurvature={0.2}
        width={800}
        height={500}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.id;
          const fontSize = 12/globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;
          const textWidth = ctx.measureText(label).width;
          const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

          ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
          ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          
          // Color coding by group (Person, Vehicle, FIR)
          if(node.group === 1) ctx.fillStyle = '#ef4444'; // Red for Person
          else if(node.group === 2) ctx.fillStyle = '#3b82f6'; // Blue for Vehicle
          else ctx.fillStyle = '#eab308'; // Yellow for FIR

          ctx.fillText(label, node.x, node.y);
          node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
        }}
        nodePointerAreaPaint={(node, color, ctx) => {
          ctx.fillStyle = color;
          const bckgDimensions = node.__bckgDimensions;
          bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
        }}
        linkColor={() => '#4b5563'}
        linkLabel="label"
      />
    </div>
  );
}
