import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import CountUp from 'react-countup';
import { X, MapPin } from 'lucide-react';

const MAP_TILE_URL = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

export default function MapDashboard() {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hoveredDistrict, setHoveredDistrict] = useState(null);

  useEffect(() => {
    const API_BASE = import.meta.env.VITE_API_URL || '/server/backend_service';
    axios.get(`${API_BASE}/api/map/districts`)
      .then(res => {
        if (res.data.status === 'success') {
          setDistricts(res.data.data);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching map data:", err);
        setLoading(false);
      });
  }, []);

  const maxCrimes = Math.max(...districts.map(d => d.total_crimes), 1);
  const totalCrimesStatewide = districts.reduce((sum, d) => sum + d.total_crimes, 0);

  return (
    <div className="flex h-full bg-gray-900 text-gray-200 overflow-hidden">
      
      {/* Sidebar Command Panel */}
      <div className="w-[380px] flex-shrink-0 bg-gray-950 border-r border-gray-800 flex flex-col z-10 shadow-2xl relative">
        <div className="p-6 border-b border-gray-800 bg-gray-900">
          <h1 className="text-2xl font-bold tracking-widest text-cyan-500 mb-1 flex items-center">
            <span className="w-2 h-2 bg-cyan-500 rounded-full mr-3 animate-pulse"></span>
            GOTHAM
          </h1>
          <p className="text-xs font-mono text-gray-500 uppercase tracking-wider">Geospatial Intelligence Unit</p>
        </div>
        
        <div className="p-6 flex-grow overflow-y-auto">
          {loading ? (
            <div className="space-y-4 opacity-50">
              <div className="h-8 bg-gray-800 rounded w-1/2 animate-pulse mb-8"></div>
              <div className="h-24 bg-gray-800 rounded w-full animate-pulse"></div>
              <div className="h-24 bg-gray-800 rounded w-full animate-pulse"></div>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              {selectedDistrict ? (
                <motion.div 
                  key="selected"
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: -20, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-1 flex items-center">
                        <MapPin className="w-4 h-4 mr-2 text-cyan-500" />
                        {selectedDistrict.district}
                      </h3>
                      <p className="text-xs font-mono text-gray-500 uppercase">Unit Analytics</p>
                    </div>
                    <button onClick={() => setSelectedDistrict(null)} className="text-gray-500 hover:text-white transition-colors">
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="bg-gray-900 rounded p-4 border border-gray-800 border-l-2 border-l-cyan-500">
                      <p className="text-xs text-gray-500 uppercase font-mono tracking-wider mb-1">Total Incidents</p>
                      <p className="text-3xl font-mono text-white">
                        <CountUp end={selectedDistrict.total_crimes} separator="," duration={1} />
                      </p>
                    </div>
                    
                    <div className="bg-gray-900 rounded p-4 border border-gray-800">
                      <div className="flex justify-between items-end mb-2">
                        <p className="text-xs text-gray-500 uppercase font-mono tracking-wider">IPC / BNS</p>
                        <p className="text-xl font-mono text-gray-300">
                          <CountUp end={selectedDistrict.ipc_crimes} separator="," duration={1} />
                        </p>
                      </div>
                      <div className="w-full bg-gray-950 h-1 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${(selectedDistrict.ipc_crimes / selectedDistrict.total_crimes) * 100}%` }}
                          transition={{ duration: 1, ease: "easeOut" }}
                          className="bg-cyan-600 h-full glow-cyan" 
                        />
                      </div>
                    </div>
                    
                    <div className="bg-gray-900 rounded p-4 border border-gray-800">
                      <div className="flex justify-between items-end mb-2">
                        <p className="text-xs text-gray-500 uppercase font-mono tracking-wider">SLL Crimes</p>
                        <p className="text-xl font-mono text-gray-300">
                          <CountUp end={selectedDistrict.sll_crimes} separator="," duration={1} />
                        </p>
                      </div>
                      <div className="w-full bg-gray-950 h-1 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${(selectedDistrict.sll_crimes / selectedDistrict.total_crimes) * 100}%` }}
                          transition={{ duration: 1, ease: "easeOut" }}
                          className="bg-blue-600 h-full" 
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-8 p-3 bg-gray-900 rounded border border-gray-800">
                    <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Confidence Basis</p>
                    <p className="text-xs text-cyan-500 font-mono">
                      Calculated from official KSP aggregates. N={<CountUp end={selectedDistrict.total_crimes} separator="," />}.
                    </p>
                  </div>
                </motion.div>
              ) : (
                <motion.div 
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="h-full flex flex-col items-center justify-center text-center px-4"
                >
                  <div className="w-12 h-12 rounded-full border border-gray-700 flex items-center justify-center mb-4">
                    <MapPin className="w-5 h-5 text-gray-600" />
                  </div>
                  <p className="text-sm text-gray-400">Select a district node on the map to initialize detailed analytics.</p>
                </motion.div>
              )}
            </AnimatePresence>
          )}
        </div>
      </div>

      {/* Map Area */}
      <div className="flex-1 relative bg-black">
        <MapContainer 
          center={[15.3173, 75.7139]} 
          zoom={7} 
          style={{ height: '100%', width: '100%', backgroundColor: '#000' }}
          zoomControl={false}
        >
          <TileLayer url={MAP_TILE_URL} attribution='&copy; CARTO' />
          
          {districts.map((d, idx) => {
            const radius = Math.max((d.total_crimes / maxCrimes) * 35, 6); 
            const isHigh = d.total_crimes > 15000;
            const isSelected = selectedDistrict?.district === d.district;
            
            return (
              <CircleMarker
                key={idx}
                center={[d.lat, d.lng]}
                radius={isSelected ? radius + 2 : radius}
                fillColor={isHigh ? "#ef4444" : "#06b6d4"}
                color={isSelected ? "#fff" : (isHigh ? "#ef4444" : "#06b6d4")}
                weight={isSelected ? 2 : 1}
                opacity={0.8}
                fillOpacity={0.4}
                eventHandlers={{
                  click: () => setSelectedDistrict(d),
                  mouseover: () => setHoveredDistrict(d),
                  mouseout: () => setHoveredDistrict(null),
                }}
              />
            );
          })}
        </MapContainer>

        {/* Custom Tooltip Overlay (Replaces Leaflet Popup for better styling) */}
        <AnimatePresence>
          {hoveredDistrict && !selectedDistrict && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="absolute bottom-6 left-6 z-[400] bg-gray-900 border border-gray-700 p-4 rounded shadow-2xl pointer-events-none min-w-[200px]"
            >
              <h4 className="text-sm font-bold text-white mb-1">{hoveredDistrict.district}</h4>
              <p className="text-xs text-gray-400 font-mono uppercase">Click to inspect node</p>
            </motion.div>
          )}
        </AnimatePresence>
        
        {/* Statewide Totals */}
        <div className="absolute top-6 right-6 z-[400] bg-gray-900 border border-gray-800 p-5 rounded shadow-2xl pointer-events-none">
          <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Statewide Volume</p>
          <p className="text-3xl font-mono text-white glow-cyan">
            {loading ? "---" : <CountUp end={totalCrimesStatewide} separator="," duration={2} />}
          </p>
        </div>
      </div>
    </div>
  );
}
