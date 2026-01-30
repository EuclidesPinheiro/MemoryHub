import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, List
from models import MemoryItem, MemoryItemCreate

DATABASE_PATH = "memoryhub.db"


def get_connection():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            app_id TEXT NOT NULL,
            user_id TEXT,
            namespace TEXT DEFAULT 'default',
            content TEXT NOT NULL,
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            expires_at TEXT
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_app_id ON memories(app_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_namespace ON memories(namespace)")
    
    conn.commit()
    conn.close()


def create_memory(data: MemoryItemCreate) -> MemoryItem:
    """Create a new memory item."""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    expires_at = None
    
    if data.ttl_seconds:
        expires_at = now + timedelta(seconds=data.ttl_seconds)
    
    memory = MemoryItem(
        app_id=data.app_id,
        user_id=data.user_id,
        namespace=data.namespace,
        content=data.content,
        tags=data.tags,
        created_at=now,
        expires_at=expires_at
    )
    
    cursor.execute("""
        INSERT INTO memories (id, app_id, user_id, namespace, content, tags, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        memory.id,
        memory.app_id,
        memory.user_id,
        memory.namespace,
        memory.content,
        json.dumps(memory.tags),
        memory.created_at.isoformat(),
        memory.expires_at.isoformat() if memory.expires_at else None
    ))
    
    conn.commit()
    conn.close()
    
    return memory


def list_memories(
    app_id: Optional[str] = None,
    user_id: Optional[str] = None,
    namespace: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50
) -> List[MemoryItem]:
    """List memories with optional filters."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM memories WHERE 1=1"
    params = []
    
    # Filter expired items
    now = datetime.now().isoformat()
    query += " AND (expires_at IS NULL OR expires_at > ?)"
    params.append(now)
    
    if app_id:
        query += " AND app_id = ?"
        params.append(app_id)
    
    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
    
    if namespace:
        query += " AND namespace = ?"
        params.append(namespace)
    
    if q:
        query += " AND (content LIKE ? OR tags LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    memories = []
    for row in rows:
        memories.append(MemoryItem(
            id=row["id"],
            app_id=row["app_id"],
            user_id=row["user_id"],
            namespace=row["namespace"],
            content=row["content"],
            tags=json.loads(row["tags"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None
        ))
    
    return memories


def delete_memory(memory_id: str) -> bool:
    """Delete a memory by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted


def get_memory(memory_id: str) -> Optional[MemoryItem]:
    """Get a single memory by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return MemoryItem(
        id=row["id"],
        app_id=row["app_id"],
        user_id=row["user_id"],
        namespace=row["namespace"],
        content=row["content"],
        tags=json.loads(row["tags"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None
    )
