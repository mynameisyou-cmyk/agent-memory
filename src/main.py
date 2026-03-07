"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import settings
from .billing.stripe_webhooks import router as billing_router
from .memory.router import router as memory_router
from .models import engine
from .ratelimit import limiter, rate_limit_handler

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("agent-memory starting up")
    yield
    logger.info("agent-memory shutting down")
    await engine.dispose()


app = FastAPI(
    title="agent-memory",
    description="Persistent memory service for AI agents. Store, retrieve, and semantically search memories across sessions.",
    version="0.1.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(memory_router)
app.include_router(billing_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "agent-memory", "version": "0.1.0"}
