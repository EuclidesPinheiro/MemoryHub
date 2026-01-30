
import { MemoryItem, CreateMemoryRequest, MemoryListResponse } from './types';

const STORAGE_KEY = 'memorycloud_db_v1';

// Helpers
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const loadDb = (): MemoryItem[] => {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : [];
};

const saveDb = (items: MemoryItem[]) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
};

// API Methods
export const mockApi = {
  async createItem(req: CreateMemoryRequest): Promise<MemoryItem> {
    await delay(300); // Network simulation
    const items = loadDb();
    
    const now = new Date();
    let expires_at = undefined;
    
    if (req.ttl_seconds) {
      const expDate = new Date(now.getTime() + req.ttl_seconds * 1000);
      expires_at = expDate.toISOString();
    }

    const newItem: MemoryItem = {
      id: `itm_${Math.random().toString(36).substr(2, 9)}`,
      app_id: req.app_id,
      user_id: req.user_id,
      namespace: req.namespace || 'default',
      content: req.content,
      tags: req.tags || [],
      created_at: now.toISOString(),
      expires_at
    };

    items.unshift(newItem); // Add to beginning
    saveDb(items);
    return newItem;
  },

  async listItems(params: {
    app_id?: string;
    user_id?: string;
    namespace?: string;
    q?: string;
    limit?: number;
  }): Promise<MemoryListResponse> {
    await delay(200);
    let items = loadDb();
    const now = new Date();

    // Filter expired
    items = items.filter(i => !i.expires_at || new Date(i.expires_at) > now);

    // Apply filters
    if (params.app_id) items = items.filter(i => i.app_id === params.app_id);
    if (params.user_id) items = items.filter(i => i.user_id === params.user_id);
    if (params.namespace) items = items.filter(i => i.namespace === params.namespace);
    
    // Search
    if (params.q) {
      const q = params.q.toLowerCase();
      items = items.filter(i => 
        i.content.toLowerCase().includes(q) || 
        i.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    // Sort by created_at desc
    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    // Limit
    const limit = params.limit || 20;
    const paginatedItems = items.slice(0, limit);

    return {
      items: paginatedItems,
      next_before: paginatedItems.length > 0 ? paginatedItems[paginatedItems.length - 1].created_at : undefined
    };
  },

  async deleteItem(id: string): Promise<void> {
    await delay(200);
    const items = loadDb();
    const newItems = items.filter(i => i.id !== id);
    saveDb(newItems);
  }
};
