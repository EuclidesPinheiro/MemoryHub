
import React, { useState, useEffect } from 'react';
import { Search, Filter, Trash2, Tag, User, Box, Clock } from 'lucide-react';
import { mockApi } from '../lib/mockApi';
import { MemoryItem } from '../lib/types';

export const Explorer: React.FC = () => {
  const [items, setItems] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    app_id: '',
    namespace: '',
    q: ''
  });

  const fetchItems = async () => {
    setLoading(true);
    try {
      // If no app_id is specified in filter, we fetch all for the dashboard view in this mock
      // In real API app_id is required, but for Explorer we relax it
      const res = await mockApi.listItems({
        app_id: filters.app_id || undefined,
        namespace: filters.namespace || undefined,
        q: filters.q || undefined,
        limit: 50
      });
      setItems(res.items);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []); // Initial load

  const handleDelete = async (id: string) => {
    if (confirm('Delete this memory item permanently?')) {
      await mockApi.deleteItem(id);
      fetchItems();
    }
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h2>Memory Explorer</h2>
          <p className="subtitle">Inspect and manage stored memories across applications.</p>
        </div>
        <button className="btn btn-primary" onClick={fetchItems}>Refresh</button>
      </header>

      <div className="filters-bar">
        <div className="filter-group">
          <Box size={16} />
          <input 
            placeholder="Filter by App ID..." 
            value={filters.app_id}
            onChange={e => setFilters({...filters, app_id: e.target.value})}
          />
        </div>
        <div className="filter-group">
          <Tag size={16} />
          <input 
            placeholder="Namespace..." 
            value={filters.namespace}
            onChange={e => setFilters({...filters, namespace: e.target.value})}
          />
        </div>
        <div className="filter-group search-group">
          <Search size={16} />
          <input 
            placeholder="Search content..." 
            value={filters.q}
            onChange={e => setFilters({...filters, q: e.target.value})}
            onKeyDown={e => e.key === 'Enter' && fetchItems()}
          />
        </div>
        <button className="btn btn-secondary" onClick={fetchItems}>Apply</button>
      </div>

      <div className="memory-list">
        {loading ? (
          <div className="loading-state">Loading memories...</div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <DatabaseIcon />
            <h3>No memories found</h3>
            <p>Try adjusting filters or create a new memory in Playground.</p>
          </div>
        ) : (
          items.map(item => (
            <div key={item.id} className="memory-card">
              <div className="memory-header">
                <span className="memory-id">{item.id}</span>
                <div className="memory-meta">
                  <span className="badge app-badge"><Box size={12}/> {item.app_id}</span>
                  {item.namespace !== 'default' && <span className="badge ns-badge">{item.namespace}</span>}
                  <span className="time-ago"><Clock size={12}/> {new Date(item.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              
              <div className="memory-content">
                {item.content}
              </div>

              <div className="memory-footer">
                <div className="tags-list">
                  {item.user_id && <span className="tag user-tag"><User size={10}/> {item.user_id}</span>}
                  {item.tags.map(t => (
                    <span key={t} className="tag">#{t}</span>
                  ))}
                </div>
                <button 
                  className="btn-icon danger" 
                  onClick={() => handleDelete(item.id)}
                  title="Delete Item"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const DatabaseIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400 mb-4">
    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
  </svg>
);
