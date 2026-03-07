"""FastAPI application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from .config import settings
from .memory.router import router as memory_router

logging.basicConfig(level=settings.log_level.upper())

app = FastAPI(
    title="agent-memory",
    description="Persistent memory service for AI agents",
    version="0.1.0",
)

app.include_router(memory_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


# TODO: add startup/shutdown events for DB + Redis connections
# TODO: add CORS middleware
# TODO: add rate limiting (slowapi)
