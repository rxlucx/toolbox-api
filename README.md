# Toolbox API

Minimal FastAPI service used as the action layer for OpenClaw.

## Endpoints

- GET /health
- POST /trade/spot (stub + guardrails)
- POST /post (stub)

Uses SQLite with WAL mode for logging and idempotency.

All real external integrations (Binance, X, Notion, Pinterest, Gumroad) will be wired later.