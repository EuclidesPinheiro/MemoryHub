from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from typing import Optional
import database
from models import MemoryItemCreate, MemoryItem, MemoryListResponse

# =============================================================================
# APP CONFIGURATION
# =============================================================================

app = FastAPI(
    title="MemoryHub API",
    description="""
## 🧠 MemoryHub - Memory Management for AI Applications

MemoryHub provides a simple yet powerful API for storing and retrieving contextual memories 
for AI assistants and chatbots.

### Features
- **Persistent Storage**: SQLite-backed memory storage
- **Tagging System**: Organize memories with custom tags
- **Namespace Support**: Isolate memories by namespace
- **TTL Support**: Automatic expiration of old memories
- **Search**: Full-text search across content and tags

### Use Cases
- Store conversation context for AI assistants
- Save user preferences and settings
- Cache frequently accessed data
- Track interaction history
    """,
    version="1.0.0",
    contact={
        "name": "MemoryHub",
        "url": "https://github.com/EuclidesPinheiro/MemoryHub",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "memories",
            "description": "Operations for creating, reading, and deleting memory items.",
        },
        {
            "name": "pages",
            "description": "HTML pages for the web dashboard.",
        },
    ]
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    database.init_db()


# =============================================================================
# HTML PAGES (Frontend)
# =============================================================================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    """Redirect to explorer."""
    return RedirectResponse(url="/explorer")


@app.get("/explorer", response_class=HTMLResponse, tags=["pages"], include_in_schema=False)
async def explorer_page(
    request: Request,
    app_id: Optional[str] = None,
    namespace: Optional[str] = None,
    q: Optional[str] = None
):
    """Explorer page - list and search memories."""
    memories = database.list_memories(app_id=app_id, namespace=namespace, q=q)
    return templates.TemplateResponse("explorer.html", {
        "request": request,
        "memories": memories,
        "filters": {"app_id": app_id or "", "namespace": namespace or "", "q": q or ""},
        "active_page": "explorer"
    })


@app.get("/playground", response_class=HTMLResponse, tags=["pages"], include_in_schema=False)
async def playground_page(request: Request):
    """Playground page - create new memories."""
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "active_page": "playground"
    })


@app.get("/docs-page", response_class=HTMLResponse, tags=["pages"], include_in_schema=False)
async def docs_page(request: Request):
    """Documentation page."""
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "active_page": "docs"
    })


# =============================================================================
# REST API ENDPOINTS
# =============================================================================

@app.post(
    "/api/memories",
    response_model=MemoryItem,
    status_code=201,
    tags=["memories"],
    summary="Create a new memory",
    description="""
Create a new memory item in the database.

The memory will be stored with a unique ID and timestamp. 
If `ttl_seconds` is provided, the memory will automatically expire after that duration.
    """,
    responses={
        201: {
            "description": "Memory created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "itm_a1b2c3d4e",
                        "app_id": "my-assistant",
                        "user_id": "user-123",
                        "namespace": "conversations",
                        "content": "User prefers dark mode",
                        "tags": ["preference", "ui"],
                        "created_at": "2024-01-30T12:00:00",
                        "expires_at": None
                    }
                }
            }
        }
    }
)
async def create_memory(data: MemoryItemCreate):
    """
    Create a new memory item with the provided data.
    
    - **app_id**: Unique identifier for your application (required)
    - **user_id**: Optional user identifier for user-specific memories
    - **namespace**: Logical grouping for memories (default: "default")
    - **content**: The actual content to store (required)
    - **tags**: List of tags for categorization
    - **ttl_seconds**: Time-to-live in seconds (optional)
    """
    memory = database.create_memory(data)
    return memory


@app.get(
    "/api/memories",
    response_model=MemoryListResponse,
    tags=["memories"],
    summary="List all memories",
    description="""
Retrieve a list of memories with optional filtering.

Memories are returned in reverse chronological order (newest first).
Expired memories are automatically excluded from results.
    """,
    responses={
        200: {
            "description": "List of memories",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "itm_a1b2c3d4e",
                                "app_id": "my-assistant",
                                "content": "User prefers dark mode",
                                "tags": ["preference"],
                                "created_at": "2024-01-30T12:00:00"
                            }
                        ],
                        "total": 1
                    }
                }
            }
        }
    }
)
async def list_memories(
    app_id: Optional[str] = Query(None, description="Filter by application ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    namespace: Optional[str] = Query(None, description="Filter by namespace"),
    q: Optional[str] = Query(None, description="Search in content and tags"),
    limit: int = Query(50, le=100, description="Maximum number of results (max: 100)")
):
    """
    List memories with optional filters.
    
    Use query parameters to filter results by app_id, user_id, namespace, 
    or perform a text search with the `q` parameter.
    """
    memories = database.list_memories(
        app_id=app_id,
        user_id=user_id,
        namespace=namespace,
        q=q,
        limit=limit
    )
    return MemoryListResponse(items=memories, total=len(memories))


@app.get(
    "/api/memories/{memory_id}",
    response_model=MemoryItem,
    tags=["memories"],
    summary="Get a memory by ID",
    description="Retrieve a specific memory item by its unique ID.",
    responses={
        200: {"description": "Memory found"},
        404: {"description": "Memory not found"}
    }
)
async def get_memory(memory_id: str):
    """
    Get a specific memory by its ID.
    
    - **memory_id**: The unique identifier of the memory (e.g., "itm_a1b2c3d4e")
    """
    memory = database.get_memory(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@app.delete(
    "/api/memories/{memory_id}",
    status_code=204,
    tags=["memories"],
    summary="Delete a memory",
    description="Permanently delete a memory item by its ID.",
    responses={
        204: {"description": "Memory deleted successfully"},
        404: {"description": "Memory not found"}
    }
)
async def delete_memory(memory_id: str):
    """
    Delete a memory by its ID.
    
    This action is permanent and cannot be undone.
    
    - **memory_id**: The unique identifier of the memory to delete
    """
    deleted = database.delete_memory(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
