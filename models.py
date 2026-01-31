from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class MemoryItemCreate(BaseModel):
    """Request model for creating a memory item."""
    app_id: str = Field(
        ...,
        description="Unique identifier for your application",
        example="my-assistant-bot"
    )
    user_id: Optional[str] = Field(
        None,
        description="Optional user identifier for user-specific memories",
        example="user-123"
    )
    namespace: str = Field(
        "default",
        description="Logical grouping for memories",
        example="conversations"
    )
    content: str = Field(
        ...,
        description="The actual content to store",
        example="User mentioned they prefer dark mode and compact view"
    )
    tags: List[str] = Field(
        default=[],
        description="List of tags for categorization",
        example=["preference", "ui-settings"]
    )
    ttl_seconds: Optional[int] = Field(
        None,
        description="Time-to-live in seconds. Memory expires after this duration.",
        example=86400,
        ge=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "app_id": "my-assistant-bot",
                "user_id": "user-123",
                "namespace": "conversations",
                "content": "User mentioned they prefer dark mode and compact view",
                "tags": ["preference", "ui-settings"],
                "ttl_seconds": 86400
            }
        }


class MemoryItem(BaseModel):
    """Complete memory item with all fields."""
    id: str = Field(
        default_factory=lambda: f"itm_{uuid.uuid4().hex[:9]}",
        description="Unique identifier for the memory item",
        example="itm_a1b2c3d4e"
    )
    app_id: str = Field(
        ...,
        description="Application ID this memory belongs to",
        example="my-assistant-bot"
    )
    user_id: Optional[str] = Field(
        None,
        description="User ID if this is a user-specific memory",
        example="user-123"
    )
    namespace: str = Field(
        "default",
        description="Namespace for organizing memories",
        example="conversations"
    )
    content: str = Field(
        ...,
        description="The stored content",
        example="User mentioned they prefer dark mode"
    )
    tags: List[str] = Field(
        default=[],
        description="Tags associated with this memory",
        example=["preference", "ui"]
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the memory was created",
        example="2024-01-30T12:00:00"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the memory will expire (null if permanent)",
        example="2024-01-31T12:00:00"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "itm_a1b2c3d4e",
                "app_id": "my-assistant-bot",
                "user_id": "user-123",
                "namespace": "conversations",
                "content": "User mentioned they prefer dark mode",
                "tags": ["preference", "ui"],
                "created_at": "2024-01-30T12:00:00",
                "expires_at": None
            }
        }


class MemoryListResponse(BaseModel):
    """Response model for listing memories."""
    items: List[MemoryItem] = Field(
        ...,
        description="List of memory items"
    )
    total: int = Field(
        ...,
        description="Total number of items returned",
        example=10
    )

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "itm_a1b2c3d4e",
                        "app_id": "my-assistant-bot",
                        "user_id": "user-123",
                        "namespace": "default",
                        "content": "User prefers dark mode",
                        "tags": ["preference"],
                        "created_at": "2024-01-30T12:00:00",
                        "expires_at": None
                    }
                ],
                "total": 1
            }
        }
