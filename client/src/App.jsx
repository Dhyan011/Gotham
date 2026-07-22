import React, { useState } from 'react'
import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import { Map, Activity, Network } from 'lucide-react'
import MapDashboard from './pages/MapDashboard'
import AnomalyDashboard from './pages/AnomalyDashboard'
import NetworkPanel from './components/NetworkPanel'
import BootSequence from './components/BootSequence'

function TopNav() {
  return (
    <div className="flex bg-gray-950 border-b border-gray-800 px-6 py-3 shadow-md z-50 relative items-center justify-between">
      <div className="flex space-x-1">
        <NavLink 
          to="/map" 
          className={({ isActive }) => `flex items-center px-4 py-2 rounded text-xs font-mono font-bold tracking-widest transition-colors ${isActive ? 'bg-gray-800 text-cyan-400' : 'text-gray-500 hover:text-gray-300 hover:bg-gray-900'}`}
        >
          <Map className="w-4 h-4 mr-2" />
          GEO-INTELLIGENCE
        </NavLink>
        <NavLink 
          to="/anomalies" 
          className={({ isActive }) => `flex items-center px-4 py-2 rounded text-xs font-mono font-bold tracking-widest transition-colors ${isActive ? 'bg-gray-800 text-cyan-400' : 'text-gray-500 hover:text-gray-300 hover:bg-gray-900'}`}
        >
          <Activity className="w-4 h-4 mr-2" />
          STATISTICAL ANOMALIES
        </NavLink>
        <NavLink 
          to="/network" 
          className={({ isActive }) => `flex items-center px-4 py-2 rounded text-xs font-mono font-bold tracking-widest transition-colors ${isActive ? 'bg-gray-800 text-cyan-400' : 'text-gray-500 hover:text-gray-300 hover:bg-gray-900'}`}
        >
          <Network className="w-4 h-4 mr-2" />
          NETWORK ANALYSIS
        </NavLink>
      </div>
      
      <div className="flex items-center space-x-2 text-[10px] font-mono text-gray-600 tracking-widest">
        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
        <span>SYS. ONLINE</span>
      </div>
    </div>
  )
}

function App() {
  const [booted, setBooted] = useState(false);

  if (!booted) {
    return <BootSequence onComplete={() => setBooted(true)} />;
  }

  return (
    <div className="flex flex-col w-screen h-screen bg-black overflow-hidden font-sans">
      <TopNav />
      <div className="flex-1 relative overflow-hidden bg-gray-900">
        <Routes>
          <Route path="/" element={<Navigate to="/map" replace />} />
          <Route path="/map" element={<MapDashboard />} />
          <Route path="/anomalies" element={<AnomalyDashboard />} />
          <Route path="/network" element={<NetworkPanel />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
