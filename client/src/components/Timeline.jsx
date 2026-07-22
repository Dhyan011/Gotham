import React from 'react';
import { Calendar, AlertCircle } from 'lucide-react';

export default function Timeline({ events }) {
  if (!events || events.length === 0) return null;

  return (
    <div className="bg-[#111111] border border-gray-800 rounded-xl p-4 mt-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-4 tracking-wider uppercase">Knowledge Timeline</h3>
      <div className="relative border-l border-gray-700 ml-3">
        {events.map((evt, idx) => (
          <div key={idx} className="mb-6 ml-6 relative">
            <span className="absolute -left-8 top-1 flex h-4 w-4 items-center justify-center rounded-full bg-blue-900 ring-4 ring-[#111111]">
              <Calendar className="h-3 w-3 text-blue-400" />
            </span>
            <div className="flex flex-col">
              <span className="text-xs text-blue-400 font-mono">{evt.date}</span>
              <p className="text-sm text-gray-300 mt-1">{evt.event}</p>
            </div>
          </div>
        ))}
        {/* Active pulse dot at the bottom */}
        <div className="absolute -left-2 -bottom-2 flex h-4 w-4 items-center justify-center rounded-full bg-red-900 animate-pulse ring-4 ring-[#111111]">
            <AlertCircle className="h-3 w-3 text-red-400" />
        </div>
      </div>
    </div>
  );
}
