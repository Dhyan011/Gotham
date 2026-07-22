import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Map, Network, Search, User, FileText, Users } from 'lucide-react';

const Sidebar = ({ role, setRole }) => {
  const roles = ['IO', 'Analyst', 'SP'];

  const navItems = [
    { name: 'Command Center', path: '/dashboard', icon: LayoutDashboard, roles: ['Analyst', 'SP'] },
    { name: 'Hotspot Map', path: '/map', icon: Map, roles: ['Analyst', 'SP'] },
    { name: 'Network Graph', path: '/network', icon: Network, roles: ['IO', 'Analyst'] },
    { name: 'Case Explorer', path: '/cases', icon: FileText, roles: ['IO', 'Analyst'] },
    { name: 'Offender Profile', path: '/offender', icon: User, roles: ['IO'] },
    { name: 'Intelligence Query', path: '/intelligence', icon: Search, roles: ['IO', 'Analyst'] },
    { name: 'Gang Analysis', path: '/gangs', icon: Users, roles: ['Analyst', 'SP'] },
  ];

  return (
    <div className="w-64 bg-gotham-bg-sec border-r border-gotham-border flex flex-col glass-panel z-10">
      <div className="p-6 flex items-center gap-3 border-b border-gotham-border">
        <div className="w-8 h-8 rounded bg-gotham-accent flex items-center justify-center font-bold text-white shadow-[0_0_15px_rgba(59,130,246,0.5)]">
          G
        </div>
        <h1 className="text-xl font-bold tracking-widest text-gotham-text">GOTHAM</h1>
      </div>

      <div className="p-4 border-b border-gotham-border">
        <label className="text-xs text-gotham-text-sec uppercase font-semibold mb-2 block">Active Role</label>
        <div className="flex bg-gotham-bg p-1 rounded border border-gotham-border">
          {roles.map(r => (
            <button
              key={r}
              onClick={() => setRole(r)}
              className={`flex-1 py-1 text-xs text-center rounded transition-all-smooth ${
                role === r ? 'bg-gotham-accent text-white shadow-md' : 'text-gotham-text-sec hover:text-white'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto p-4 space-y-2">
        {navItems.filter(item => item.roles.includes(role)).map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all-smooth ${
                isActive
                  ? 'bg-gotham-card text-gotham-accent border border-gotham-accent/30 shadow-[0_0_10px_rgba(59,130,246,0.1)]'
                  : 'text-gotham-text hover:bg-gotham-card hover:text-gotham-accent'
              }`
            }
          >
            <item.icon size={18} />
            <span className="font-medium text-sm">{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
