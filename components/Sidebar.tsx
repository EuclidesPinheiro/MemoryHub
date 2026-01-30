
import React from 'react';
import { Layout, Database, Terminal, FileText, Cloud } from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentPage, onNavigate }) => {
  const navItems = [
    { id: 'explorer', label: 'Explorer', icon: Database },
    { id: 'playground', label: 'Playground', icon: Terminal },
    { id: 'docs', label: 'Backend Code', icon: FileText },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <Cloud className="logo-icon" size={28} />
        <h1>MemoryCloud</h1>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <p>MVP v0.1.0</p>
      </div>
    </div>
  );
};
