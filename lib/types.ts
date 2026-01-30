
export interface MemoryItem {
  id: string;
  app_id: string;
  user_id?: string;
  namespace: string;
  content: string;
  tags: string[];
  created_at: string;
  expires_at?: string;
}

export interface CreateMemoryRequest {
  app_id: string;
  user_id?: string;
  namespace?: string;
  content: string;
  tags?: string[];
  ttl_seconds?: number;
}

export interface MemoryListResponse {
  items: MemoryItem[];
  next_before?: string;
}

export interface ApiError {
  error: string;
}
