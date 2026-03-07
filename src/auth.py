"""API key authentication middleware."""

from __future__ import annotations

import uuid

import bcrypt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Project, async_session

security = HTTPBearer()


def hash_api_key(key: str) -> str:
    """Hash an API key for storage."""
    return bcrypt.hashpw(key.encode(), bcrypt.gensalt()).decode()


def verify_api_key(key: str, hashed: str) -> bool:
    """Verify a plaintext key against its hash."""
    return bcrypt.checkpw(key.encode(), hashed.encode())


async def get_db() -> AsyncSession:
    """Yield an async database session."""
    async with async_session() as session:
        yield session


async def get_project(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
) -> Project:
    """Validate API key and return the associated project."""
    # TODO: implement proper lookup (currently linear scan — fine for MVP, index later)
    token = credentials.credentials
    result = await db.execute(select(Project))
    for project in result.scalars():
        if verify_api_key(token, project.api_key):
            return project
    raise HTTPException(status_code=401, detail="Invalid API key")
