# Deployment Guide

This project now targets Supabase-managed PostgreSQL for persistence and assumes a container-based deployment. The steps below cover the minimum configuration needed to run Aria (Aria) with authentication and billing enabled.

## 1. Required Environment Variables
Set these variables in your deployment platform:

- `SUPABASE_DB_URL` – Supabase PostgreSQL connection string (format: `postgresql://...`).
- `SESSION_SECRET` – Random 32+ character string for Flask session security.
- `FLASK_SECRET_KEY` – Secret key used by Flask to sign cookies.
- `STRIPE_SECRET_KEY` – Stripe secret key for billing.
- `STRIPE_WEBHOOK_SECRET` – Stripe webhook signing secret.
- `PUBLIC_URL` – Public base URL of the deployment (e.g., `https://aria.example.com`).
- `API_KEY` – Optional API key for protected endpoints.

## 2. Database Configuration
Supabase provides a managed Postgres instance. Copy the connection string from Supabase and set it as `SUPABASE_DB_URL`. The application automatically:

- Normalizes `postgres://` URLs for SQLAlchemy.
- Applies lightweight migrations to create required tables.
- Uses conservative pool sizes appropriate for hosted Postgres.

## 3. Stripe Billing
Stripe integration is enabled when `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are set.

- Success URL: `${PUBLIC_URL}/payment-success?session_id={CHECKOUT_SESSION_ID}`
- Cancel URL: `${PUBLIC_URL}/payment`
- Webhook endpoint: `${PUBLIC_URL}/webhook`

## 4. Running Locally
1. Create a `.env` file with the variables above.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the app: `python run_ui.py --host=0.0.0.0 --port=5000`.

## 5. Production Notes
- Use `scripts/start_production.sh` as the container entrypoint; it runs migrations and starts Gunicorn when available.
- Set `PORT` to the exposed port in your platform.
- Keep `SESSION_SECRET` and `FLASK_SECRET_KEY` unique per environment.

## 6. Troubleshooting
- **Database connectivity issues**: verify `SUPABASE_DB_URL` and that the Supabase instance is running.
- **Stripe errors**: ensure both `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are configured.
- **Auth failures**: confirm session secrets are set and cookies are allowed by your domain.
