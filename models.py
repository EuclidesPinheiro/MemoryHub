from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class MemoryItemCreate(BaseModel):
    """Request model for creating a memory item."""
    app_id: str
    user_id: Optional[str] = None
    namespace: str = "default"
    content: str
    tags: List[str] = []
    ttl_seconds: Optional[int] = None


class MemoryItem(BaseModel):
    """Complete memory item with all fields."""
    id: str = Field(default_factory=lambda: f"itm_{uuid.uuid4().hex[:9]}")
    app_id: str
    user_id: Optional[str] = None
    namespace: str = "default"
    content: str
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemoryListResponse(BaseModel):
    """Response model for listing memories."""
    items: List[MemoryItem]
    total: int
