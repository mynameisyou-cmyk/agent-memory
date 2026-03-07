# agent-memory — Implementation TODO

Ordered by dependency. Work top to bottom.

## Phase 2 — Scaffold
- [ ] [S] Init pyproject.toml (FastAPI, SQLAlchemy, pgvector, redis, pydantic, openai)
- [ ] [S] Create directory structure per ARCHITECTURE.md
- [ ] [S] Write stub files (main.py, config.py, auth.py, models.py, embed.py)
- [ ] [T] Write .env.example
- [ ] [T] Write docker-compose.yml (postgres 16 + pgvector, redis)
- [ ] [S] Write 001_initial.sql migration (projects, memories, usage_events tables)

## Phase 3 — Core Build
- [ ] [S] config.py — env var loading, settings validation
- [ ] [S] models.py — SQLAlchemy ORM models + DB session factory
- [ ] [S] auth.py — API key hashing, validation middleware
- [ ] [S] embed.py — OpenAI embedding wrapper with retry + caching
- [ ] [S] memory/schemas.py — Pydantic models for all request/response shapes
- [ ] [S] memory/service.py — write() logic (embed + insert + usage event)
- [ ] [S] memory/service.py — read_by_id() and read_by_key()
- [ ] [C] search/vector.py — pgvector cosine search query
- [ ] [S] search/rerank.py — importance × recency reranking
- [ ] [S] memory/service.py — search() (vector search → rerank → return)
- [ ] [S] memory/service.py — delete() by id and by key
- [ ] [S] memory/router.py — wire all routes to service
- [ ] [S] cache/redis.py — working memory TTL store + read cache
- [ ] [S] billing/usage.py — usage event writer
- [ ] [S] main.py — app factory, middleware, router registration

## Phase 3 — Tests
- [ ] [S] tests/test_memory.py — write, read, delete
- [ ] [S] tests/test_search.py — semantic search accuracy check
- [ ] [S] tests/test_auth.py — invalid key rejection

## Phase 4 — Integration
- [ ] [S] Dockerfile (multi-stage, non-root)
- [ ] [S] DEPLOY.md — Railway deploy steps
- [ ] [S] Stripe webhook handler (payment_failed → plan downgrade)
- [ ] [S] /v1/usage endpoint
- [ ] [S] Rate limiting per plan (slowapi)
- [ ] [S] OpenAPI docs polish (descriptions, examples)

## Phase 5 — Live
- [ ] [C] Deploy to Railway (postgres + redis + API)
- [ ] [S] Set up Stripe product + pricing tiers
- [ ] [T] Landing page (simple, direct — what it is, pricing, get API key)
- [ ] [T] Update DEVICE.md → stream status "live"
- [ ] [T] Message Yu with live URL
