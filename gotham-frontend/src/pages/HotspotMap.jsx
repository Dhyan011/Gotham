import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import TemporalSlider from '../components/TemporalSlider';
import { crimeTypeColors } from '../utils/colorScale';

const HotspotMap = () => {
  const position = [12.9716, 77.5946]; 

  return (
    <div className="flex gap-4 h-[calc(100vh-7rem)]">
      <div className="w-64 glass-panel p-4 rounded-xl flex flex-col gap-6">
        <div>
          <h3 className="text-sm font-semibold mb-3">Filters</h3>
          <div className="space-y-2">
            {Object.keys(crimeTypeColors).map(type => (
              <label key={type} className="flex items-center gap-2 text-sm cursor-pointer hover:text-white transition-colors">
                <input type="checkbox" defaultChecked className="accent-gotham-accent" />
                <span className="w-2 h-2 rounded-full shadow-[0_0_5px_currentColor]" style={{ backgroundColor: crimeTypeColors[type], color: crimeTypeColors[type] }}></span>
                {type}
              </label>
            ))}
          </div>
        </div>
        
        <div className="mt-auto">
          <h3 className="text-sm font-semibold mb-3">Timeline</h3>
          <TemporalSlider />
        </div>
      </div>
      
      <div className="flex-1 glass-card rounded-xl overflow-hidden relative border border-gotham-border">
        <MapContainer center={position} zoom={11} className="w-full h-full z-0">
          <TileLayer
            url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
            attribution='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />
          <CircleMarker center={[12.97, 77.59]} radius={25} pathOptions={{ color: '#EF4444', fillColor: '#EF4444', fillOpacity: 0.4, weight: 1 }}>
            <Popup className="bg-gotham-card text-gotham-text border-gotham-border">High Activity Cluster</Popup>
          </CircleMarker>
          <CircleMarker center={[13.0, 77.62]} radius={15} pathOptions={{ color: '#F59E0B', fillColor: '#F59E0B', fillOpacity: 0.4, weight: 1 }} />
        </MapContainer>
        
        <div className="absolute bottom-4 right-4 bg-gotham-bg/90 backdrop-blur p-3 rounded-lg border border-gotham-border text-xs z-[1000] shadow-lg">
          <h4 className="font-semibold mb-2">Cluster Density</h4>
          <div className="flex items-center gap-2 mb-1"><span className="w-3 h-3 bg-gotham-danger/60 rounded"></span> High (>50)</div>
          <div className="flex items-center gap-2"><span className="w-3 h-3 bg-gotham-warning/60 rounded"></span> Medium (20-50)</div>
        </div>
      </div>
    </div>
  );
};

export default HotspotMap;
