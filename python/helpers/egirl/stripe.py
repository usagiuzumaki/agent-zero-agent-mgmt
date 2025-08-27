import os, logging
try:
    import stripe
except Exception as e:  # pragma: no cover - optional dependency
    stripe = None
    logging.error("Stripe library not available: %s", e)

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY")
if stripe:
    stripe.api_key = STRIPE_KEY

def create_checkout_session(price_id: str, success_url: str | None = None, cancel_url: str | None = None):
    if not stripe or not stripe.api_key:
        logging.error("Stripe not configured.")
        return None
    domain = os.getenv("DOMAIN_URL", "http://localhost:8000")
    success_url = success_url or f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = cancel_url or f"{domain}/cancel"
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session.url
    except Exception as e:
        logging.exception("Stripe error: %s", e)
        return None


def create_subscription_session(price_id: str, success_url: str | None = None, cancel_url: str | None = None):
    """Create a Stripe checkout session for subscriptions."""
    if not stripe or not stripe.api_key:
        logging.error("Stripe not configured.")
        return None
    domain = os.getenv("DOMAIN_URL", "http://localhost:8000")
    success_url = success_url or f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = cancel_url or f"{domain}/cancel"
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url
    except Exception as e:
        logging.exception("Stripe subscription error: %s", e)
        return None


def create_refund(payment_intent: str):
    """Issue a refund for a given payment intent."""
    if not stripe or not stripe.api_key:
        logging.error("Stripe not configured.")
        return None
    try:
        refund = stripe.Refund.create(payment_intent=payment_intent)
        return refund.id
    except Exception as e:
        logging.exception("Stripe refund error: %s", e)
        return None


def create_payout(amount: int, currency: str = "usd"):
    """Create a payout to the connected account."""
    if not stripe or not stripe.api_key:
        logging.error("Stripe not configured.")
        return None
    try:
        payout = stripe.Payout.create(amount=amount, currency=currency)
        return payout.id
    except Exception as e:
        logging.exception("Stripe payout error: %s", e)
        return None
