# Aria Reality Map

## Architecture Overview
- **Server Stack**: Flask (WSGI) as the primary web server, Starlette (ASGI) for MCP via `a2wsgi` bridge.
- **Frontend**: React-based UI (in `ui-kit-react`) or legacy HTML (in `webui`).
- **Database**: Postgres (Supabase) for user/auth, SQLite (`loom.db`) for local agent state.

## Entrypoints
- `run_ui.py`: Main server start script. Port 5000 by default.
- `python/api/`: Directory containing modular API handlers.

## Auth & Billing Flow
1. **Login**: User logs in via Google OAuth or Email/Password (`supabase_auth.py`).
2. **Paywall**: Redirected to `/payment/required` if `has_paid` is false.
3. **Checkout**: Stripe Checkout session created (`stripe_payments.py`).
4. **Provisioning**: Stripe Webhook (`checkout.session.completed`) updates user status in DB.

## Agent Routing
- Logic resides in `agents/agent.py`.
- **Tool Selection**: Hierarchical lookup: MCP -> Profile -> Default -> Screenwriting.
- **Delegation**: Manual via `call_sub` tool. No automated router or strict budget enforcement currently exists.

## Production Risks (Likelihood x Impact)
1. **Endless Delegation**: Recursive agent calls without depth/budget limits. (High)
2. **Secret Leakage**: `PrintStyle` logging potentially sensitive data. (High)
3. **Webhook Idempotency**: Risk of double-processing Stripe events. (Medium)
4. **Config Fragility**: Startup fails to validate all required environment variables. (Medium)
5. **Rate Limiting**: Missing basic abuse protection on public endpoints. (Medium)
6. **Side-Effect Safety**: No "Safe Mode" to prevent accidental production posts/charges during dev. (Medium)
7. **DB Pooling**: Potential for connection exhaustion under load. (Low)
8. **Logging Quality**: Lack of structured logs makes log aggregation difficult. (Low)
9. **Error Boundaries**: Some exceptions might not be caught cleanly at the boundary. (Low)
10. **MCP Isolation**: Starlette mount might bypass some Flask-level auth logic. (Low)
