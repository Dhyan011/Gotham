import React from 'react';
import { Bell, Search, UserCircle } from 'lucide-react';
import { useLocation } from 'react-router-dom';

const TopBar = ({ role }) => {
  const location = useLocation();
  const getPageTitle = () => {
    const path = location.pathname.substring(1);
    if (!path) return 'Dashboard';
    return path.charAt(0).toUpperCase() + path.slice(1);
  };

  return (
    <div className="h-16 bg-gotham-bg-sec border-b border-gotham-border flex items-center justify-between px-6 glass-panel z-10 sticky top-0">
      <h2 className="text-lg font-semibold text-gotham-text capitalize">{getPageTitle()}</h2>
      
      <div className="flex items-center gap-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gotham-text-sec" size={16} />
          <input 
            type="text" 
            placeholder="Search entities, cases, officers..." 
            className="bg-gotham-bg border border-gotham-border rounded-full py-1.5 pl-10 pr-4 text-sm w-64 focus:outline-none focus:border-gotham-accent text-gotham-text transition-all-smooth placeholder:text-gotham-text-sec"
          />
        </div>

        <div className="relative cursor-pointer">
          <Bell className="text-gotham-text hover:text-white transition-colors" size={20} />
          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-gotham-danger rounded-full pulse-alert border-2 border-gotham-bg-sec"></span>
        </div>

        <div className="flex items-center gap-2 border-l border-gotham-border pl-6">
          <UserCircle className="text-gotham-accent" size={24} />
          <div className="flex flex-col">
            <span className="text-xs font-semibold">{role} Officer</span>
            <span className="text-[10px] text-gotham-text-sec">ID: KSP-8842</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
