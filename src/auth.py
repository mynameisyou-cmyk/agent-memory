"""API key authentication middleware.

Validates keys against the tools schema (shared across all AgentTool services).
Falls back to local memory schema if AUTH_DATABASE_URL not configured.
"""

from __future__ import annotations

import uuid

import bcrypt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .config import settings
from .models import async_session

security = HTTPBearer()

# Auth engine — points to tools schema for shared API key validation
_auth_engine = None
_auth_session = None

def _get_auth_session():
    global _auth_engine, _auth_session
    if _auth_session is None:
        url = settings.auth_database_url or settings.database_url
        _auth_engine = create_async_engine(url, echo=False, pool_size=2, max_overflow=2)
        _auth_session = async_sessionmaker(_auth_engine, class_=AsyncSession, expire_on_commit=False)
    return _auth_session


def hash_api_key(key: str) -> str:
    """Hash an API key for storage (bcrypt)."""
    return bcrypt.hashpw(key.encode(), bcrypt.gensalt()).decode()


def verify_api_key(key: str, hashed: str) -> bool:
    """Verify a plaintext key against its bcrypt hash."""
    return bcrypt.checkpw(key.encode(), hashed.encode())


async def get_db() -> AsyncSession:
    """Yield an async database session (memory schema)."""
    async with async_session() as session:
        yield session


class ProjectContext:
    """Lightweight project info from the tools schema."""
    def __init__(self, project_id: uuid.UUID, name: str, plan: str, credits: int):
        self.id = project_id
        self.name = name
        self.plan = plan
        self.credits = credits


async def get_project(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
) -> ProjectContext:
    """Validate API key against tools schema and return the associated project."""
    token = credentials.credentials

    auth_sess = _get_auth_session()
    async with auth_sess() as auth_db:
        # Look up by key_prefix first (fast), then bcrypt verify
        prefix = token[:11] if len(token) >= 11 else token
        result = await auth_db.execute(
            text("SELECT ak.key_hash, p.id, p.name, p.plan, p.credits "
                 "FROM tools.api_keys ak "
                 "JOIN tools.projects p ON p.id = ak.project_id "
                 "WHERE ak.key_prefix = :prefix AND ak.revoked_at IS NULL"),
            {"prefix": prefix}
        )
        rows = result.fetchall()
        for row in rows:
            if verify_api_key(token, row.key_hash):
                return ProjectContext(
                    project_id=row.id,
                    name=row.name,
                    plan=row.plan,
                    credits=row.credits,
                )

    raise HTTPException(status_code=401, detail="Invalid API key")
