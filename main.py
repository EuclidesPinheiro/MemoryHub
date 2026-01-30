from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
import database
from models import MemoryItemCreate, MemoryItem, MemoryListResponse

# Initialize app
app = FastAPI(title="MemoryHub", description="Memory management dashboard for AI applications")

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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Redirect to explorer."""
    return RedirectResponse(url="/explorer")


@app.get("/explorer", response_class=HTMLResponse)
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


@app.get("/playground", response_class=HTMLResponse)
async def playground_page(request: Request):
    """Playground page - create new memories."""
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "active_page": "playground"
    })


@app.get("/docs-page", response_class=HTMLResponse)
async def docs_page(request: Request):
    """Documentation page."""
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "active_page": "docs"
    })


# =============================================================================
# REST API ENDPOINTS
# =============================================================================

@app.post("/api/memories", response_model=MemoryItem, status_code=201)
async def create_memory(data: MemoryItemCreate):
    """Create a new memory item."""
    memory = database.create_memory(data)
    return memory


@app.get("/api/memories", response_model=MemoryListResponse)
async def list_memories(
    app_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    namespace: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(50, le=100)
):
    """List memories with optional filters."""
    memories = database.list_memories(
        app_id=app_id,
        user_id=user_id,
        namespace=namespace,
        q=q,
        limit=limit
    )
    return MemoryListResponse(items=memories, total=len(memories))


@app.get("/api/memories/{memory_id}", response_model=MemoryItem)
async def get_memory(memory_id: str):
    """Get a specific memory by ID."""
    memory = database.get_memory(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@app.delete("/api/memories/{memory_id}", status_code=204)
async def delete_memory(memory_id: str):
    """Delete a memory by ID."""
    deleted = database.delete_memory(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
