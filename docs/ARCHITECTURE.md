# Aria Architecture

## Overview
Aria is a multi-agent creative companion designed for production deployment. It uses a hybrid web architecture to balance ease of use with robust API capabilities.

## Web Stack
- **Primary Server**: Flask (WSGI)
  - Responsibilities: UI serving, Session management, Authentication, Custom API handlers, Stripe integration.
- **API Bridge**: FastAPI/Starlette (ASGI)
  - Responsibilities: Model Context Protocol (MCP) server hosting.
- **Integration**: `a2wsgi` is used to bridge the ASGI MCP server into the Flask WSGI application via `DispatcherMiddleware`.

## Data Layer
- **Postgres (via Supabase)**: Primary data store for users and persistent state.
- **SQLite (loom.db)**: Local storage for interaction events and behavioral patterns.

## Agent System
- **Core Agent**: Located in `agents/agent.py`.
- **Registry**: Managed by `python/helpers/agent_registry.py` (Planned).
- **Tooling**: Extensible tool system with local and MCP-based tool discovery.

## Security & Reliability
- **Auth**: Supabase Auth integration.
- **Billing**: Stripe with signature verification and idempotency.
- **Operational Safe Mode**: Env flag `OPERATIONAL_SAFE_MODE=true` to disable external side effects.
- **Monitoring**: `/healthz` and `/readyz` endpoints for orchestration.
