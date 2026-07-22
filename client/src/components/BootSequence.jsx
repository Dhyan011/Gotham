import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function BootSequence({ onComplete }) {
  const [text, setText] = useState('');
  const fullText = "INITIALIZING GOTHAM INTELLIGENCE ENGINE...";
  
  useEffect(() => {
    let i = 0;
    const timer = setInterval(() => {
      setText(fullText.slice(0, i));
      i++;
      if (i > fullText.length) {
        clearInterval(timer);
        setTimeout(onComplete, 500);
      }
    }, 40);
    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <div className="flex flex-col items-center justify-center w-screen h-screen bg-black text-cyan-500 font-mono">
      <motion.div 
        initial={{ opacity: 0 }} 
        animate={{ opacity: 1 }} 
        className="w-1/2 max-w-lg"
      >
        <div className="text-sm mb-4 tracking-widest uppercase opacity-70">SCRB Secure Connection Established</div>
        <div className="h-6 text-xl tracking-[0.2em]">{text}<span className="animate-pulse">_</span></div>
        
        <div className="mt-8 space-y-2 opacity-50 text-xs">
          <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.2 }}>[OK] Loading geospatial boundary data...</motion.div>
          <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.6 }}>[OK] Syncing real-time KSP aggregate metrics...</motion.div>
          <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 1.0 }}>[OK] Calibrating anomaly detection heuristics...</motion.div>
          <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 1.4 }}>[OK] Bypassing entity-resolution (Insufficient Granularity)...</motion.div>
        </div>
      </motion.div>
    </div>
  );
}
