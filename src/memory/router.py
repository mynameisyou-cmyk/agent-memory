"""FastAPI router for /v1/memories endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1/memories", tags=["memories"])

# TODO: implement routes in core-build phase
# POST   /              → create memory
# GET    /{memory_id}   → read by id
# GET    /?key=&agent_id= → read by key
# POST   /search        → semantic search
# DELETE /{memory_id}   → delete by id
# DELETE /?key=         → delete by key
