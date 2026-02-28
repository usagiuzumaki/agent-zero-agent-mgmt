# Aria Runbook

## Deployment
1. **Provision Infrastructure**: Ensure a Postgres database (e.g., Supabase) and Stripe account are available.
2. **Configure Environment**: Set all required variables in `.env`.
   - `SESSION_SECRET` (Critical)
   - `SUPABASE_DB_URL` (For Auth/Persistence)
   - `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` (For Payments)
3. **Build & Launch**:
   ```bash
   make run
   ```
   The server will fail-fast if `SESSION_SECRET` is missing.

## Health Monitoring
- **Shallow Health**: `GET /healthz` (Returns 200 if Flask is up).
- **Readiness Check**: `GET /readyz` (Returns 200 if DB and Config are valid).

## Operational Modes
- **Production Mode**: Default behavior. Side effects like Stripe charges are enabled.
- **Safe Mode**: Set `OPERATIONAL_SAFE_MODE=true` to block external side effects while keeping the app usable for development or testing.

## Incident Management
- **Database Connection Issues**: Check `SUPABASE_DB_URL` and verify that the endpoint is not disabled or sleeping.
- **Stripe Webhook Failures**: Verify `STRIPE_WEBHOOK_SECRET`. Check logs for "Duplicate Stripe event skipped" to confirm idempotency is working.
- **Agent Loops**: If an agent exceeds its budget, it will return a "Budget exceeded" warning. Check the `AgentRegistry` in `python/helpers/agent_registry.py` to adjust limits.

## Secret Rotation
1. Update the secret in the environment/secret manager.
2. Restart the application.
3. Verification: Verify that `/readyz` returns 200 after rotation.

## Rollback
1. Revert to the previous stable commit.
2. Ensure database schema remains compatible (migrations are currently deterministic and additive).
3. Restart the service.
