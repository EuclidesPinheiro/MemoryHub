
import React, { useState } from 'react';
import { Send, Plus, X } from 'lucide-react';
import { mockApi } from '../lib/mockApi';

export const Playground: React.FC = () => {
  const [form, setForm] = useState({
    app_id: 'my-assistant-bot',
    user_id: '',
    namespace: 'default',
    content: '',
    ttl_seconds: 2592000 // 30 days default
  });
  const [currentTag, setCurrentTag] = useState('');
  const [tags, setTags] = useState<string[]>(['test']);
  const [status, setStatus] = useState<'idle' | 'saving' | 'success'>('idle');
  const [lastResponse, setLastResponse] = useState<string>('');

  const handleAddTag = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && currentTag.trim()) {
      e.preventDefault();
      if (!tags.includes(currentTag.trim())) {
        setTags([...tags, currentTag.trim()]);
      }
      setCurrentTag('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter(t => t !== tagToRemove));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('saving');
    
    try {
      const response = await mockApi.createItem({
        ...form,
        tags
      });
      
      setLastResponse(JSON.stringify(response, null, 2));
      setStatus('success');
      // Reset content only, keep config
      setForm(prev => ({ ...prev, content: '' }));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="page-container playground-container">
      <div className="playground-grid">
        {/* Input Column */}
        <div className="panel input-panel">
          <div className="panel-header">
            <h3>Create Memory Item</h3>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>App ID *</label>
                <input 
                  required
                  value={form.app_id}
                  onChange={e => setForm({...form, app_id: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>User ID</label>
                <input 
                  value={form.user_id}
                  onChange={e => setForm({...form, user_id: e.target.value})}
                  placeholder="Optional"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Namespace</label>
                <input 
                  value={form.namespace}
                  onChange={e => setForm({...form, namespace: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>TTL (Seconds)</label>
                <input 
                  type="number"
                  value={form.ttl_seconds}
                  onChange={e => setForm({...form, ttl_seconds: parseInt(e.target.value)})}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Tags (Press Enter)</label>
              <div className="tags-input-container">
                {tags.map(tag => (
                  <span key={tag} className="tag-chip">
                    {tag}
                    <button type="button" onClick={() => removeTag(tag)}><X size={12}/></button>
                  </span>
                ))}
                <input 
                  value={currentTag}
                  onChange={e => setCurrentTag(e.target.value)}
                  onKeyDown={handleAddTag}
                  placeholder="Add tag..."
                />
              </div>
            </div>

            <div className="form-group">
              <label>Content *</label>
              <textarea 
                required
                rows={6}
                value={form.content}
                onChange={e => setForm({...form, content: e.target.value})}
                placeholder="Enter text or JSON content to store..."
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary full-width" disabled={status === 'saving'}>
                {status === 'saving' ? 'Saving...' : (
                  <>
                    <Send size={16} /> Store Memory
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Output Column */}
        <div className="panel output-panel">
          <div className="panel-header">
            <h3>API Response</h3>
            {status === 'success' && <span className="status-badge success">201 Created</span>}
          </div>
          <div className="code-viewer">
            {lastResponse ? (
              <pre>{lastResponse}</pre>
            ) : (
              <div className="placeholder-text">
                Waiting for request...
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
