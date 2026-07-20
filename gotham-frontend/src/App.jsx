import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import CommandCenter from './pages/CommandCenter';
import HotspotMap from './pages/HotspotMap';
import NetworkGraph from './pages/NetworkGraph';
import CaseExplorer from './pages/CaseExplorer';
import OffenderProfile from './pages/OffenderProfile';
import IntelligenceQuery from './pages/IntelligenceQuery';
import GangAnalysis from './pages/GangAnalysis';

function App() {
  const [role, setRole] = useState('Analyst'); // IO, Analyst, SP

  return (
    <div className="flex h-screen overflow-hidden bg-gotham-bg text-gotham-text">
      <Sidebar role={role} setRole={setRole} />
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar role={role} />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gotham-bg p-4">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<CommandCenter />} />
            <Route path="/map" element={<HotspotMap />} />
            <Route path="/network" element={<NetworkGraph />} />
            <Route path="/cases" element={<CaseExplorer />} />
            <Route path="/offender" element={<OffenderProfile />} />
            <Route path="/intelligence" element={<IntelligenceQuery />} />
            <Route path="/gangs" element={<GangAnalysis />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
