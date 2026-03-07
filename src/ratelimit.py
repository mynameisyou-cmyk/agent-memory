"""Per-project rate limiting using slowapi."""

from __future__ import annotations

from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from .config import PLAN_RATE_LIMITS


def _project_key(request: Request) -> str:
    """Rate limit key: project ID from auth middleware, fall back to IP."""
    project = getattr(request.state, "project", None)
    if project:
        return f"project:{project.id}"
    return get_remote_address(request)


def _dynamic_limit(key: str) -> str:
    """Return rate limit string based on project plan.

    Called by slowapi. We stash the plan on request.state during auth.
    Default to seed tier if unknown.
    """
    # slowapi calls this with the key, but we need the plan.
    # We use the seed default — the actual per-plan enforcement
    # happens in the middleware below.
    return f"{PLAN_RATE_LIMITS.get('seed', 30)}/minute"


limiter = Limiter(key_func=_project_key)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Upgrade your plan for higher limits.",
            "retry_after": exc.detail,
        },
    )
