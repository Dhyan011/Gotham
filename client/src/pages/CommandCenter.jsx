import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import AlertBanner from '../components/AlertBanner';
import { mockStats, mockCrimeTypes, mockDistricts, mockRecentFirs } from '../utils/mockData';
import { crimeTypeColors, getSeverityColor } from '../utils/colorScale';

const CommandCenter = () => {
  return (
    <div className="space-y-6">
      <AlertBanner />
      
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total FIRs', value: mockStats.totalFirs },
          { label: 'Active Cases', value: mockStats.activeCases },
          { label: 'Arrests', value: mockStats.arrests },
          { label: 'Active Alerts', value: mockStats.activeAlerts, color: 'text-gotham-danger' }
        ].map((stat, i) => (
          <div key={i} className="glass-card p-4 rounded-xl border-t-2 border-t-gotham-accent/50">
            <h3 className="text-gotham-text-sec text-sm">{stat.label}</h3>
            <p className={`text-3xl font-bold mt-2 ${stat.color || 'text-gotham-text'}`}>
              {stat.value.toLocaleString()}
            </p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="glass-panel p-4 rounded-xl h-80">
          <h3 className="text-sm font-semibold mb-4">Crime Distribution</h3>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={mockCrimeTypes}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {mockCrimeTypes.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={crimeTypeColors[entry.name]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1C2333', border: '1px solid #2D3748', borderRadius: '8px' }}
                itemStyle={{ color: '#F9FAFB' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-panel p-4 rounded-xl h-80">
          <h3 className="text-sm font-semibold mb-4">Top Districts</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={mockDistricts} layout="vertical" margin={{ left: 40 }}>
              <XAxis type="number" hide />
              <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fill: '#9CA3AF', fontSize: 12 }} />
              <Tooltip cursor={{ fill: '#2D3748' }} contentStyle={{ backgroundColor: '#1C2333', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="#3B82F6" radius={[0, 4, 4, 0]} barSize={20} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-panel p-4 rounded-xl">
        <h3 className="text-sm font-semibold mb-4">Recent FIRs</h3>
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-gotham-text-sec uppercase bg-gotham-bg/50">
            <tr>
              <th className="px-4 py-3 rounded-tl-lg">FIR ID</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">District</th>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3 rounded-tr-lg">Status</th>
            </tr>
          </thead>
          <tbody>
            {mockRecentFirs.map((fir, i) => (
              <tr key={i} className="border-b border-gotham-border/50 hover:bg-gotham-card/50 transition-colors">
                <td className="px-4 py-3 font-mono text-gotham-accent">{fir.id}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded text-xs border" style={{ backgroundColor: `${crimeTypeColors[fir.type]}10`, borderColor: `${crimeTypeColors[fir.type]}40`, color: crimeTypeColors[fir.type] }}>
                    {fir.type}
                  </span>
                </td>
                <td className="px-4 py-3">{fir.district}</td>
                <td className="px-4 py-3 text-gotham-text-sec">{fir.date}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded text-xs border ${fir.status === 'Active' ? 'bg-gotham-warning/10 border-gotham-warning/40 text-gotham-warning' : 'bg-gotham-success/10 border-gotham-success/40 text-gotham-success'}`}>
                    {fir.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CommandCenter;
