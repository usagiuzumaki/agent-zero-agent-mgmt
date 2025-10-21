import importlib
import logging
import os
import subprocess
import sys
from typing import Optional

from python.helpers import dotenv

try:  # pragma: no cover - optional dependency during runtime
    import stripe  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - dependency missing
    stripe = None  # type: ignore[assignment]


_DOMAIN_FALLBACK = "http://localhost:8000"
_STRIPE_INITIALISED = False

_LOGGER = logging.getLogger(__name__)


def _ensure_stripe() -> "stripe":
    """Return the configured ``stripe`` module or raise a helpful error."""

    global stripe

    if stripe is None:
        _install_stripe_package()
        try:
            stripe = importlib.import_module("stripe")  # type: ignore[assignment]
        except ModuleNotFoundError as exc:  # pragma: no cover - unexpected failure
            raise RuntimeError(
                "Stripe integration requires the optional 'stripe' package. "
                "Automatic installation failed; install it manually with `pip install stripe`."
            ) from exc

    global _STRIPE_INITIALISED
    if not _STRIPE_INITIALISED:
        dotenv.load_dotenv()
        key = (os.getenv("STRIPE_SECRET_KEY") or "").strip()
        if not key:
            raise RuntimeError(
                "STRIPE_SECRET_KEY is not configured. Add it to your environment or "
                "the project .env file to enable Stripe actions."
            )
        stripe.api_key = key
        _STRIPE_INITIALISED = True
    return stripe


def _install_stripe_package() -> None:
    """Ensure the ``stripe`` package is installed before use."""

    _LOGGER.warning(
        "Stripe python package not found. Attempting automatic installation..."
    )
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "stripe"])
    except subprocess.CalledProcessError as exc:  # pragma: no cover - subprocess failure
        raise RuntimeError(
            "Stripe integration requires the optional 'stripe' package. "
            "Automatic installation failed; install it manually with `pip install stripe`."
        ) from exc


def _domain_url() -> str:
    return os.getenv("DOMAIN_URL", _DOMAIN_FALLBACK)


def create_checkout_session(
    price_id: str,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
) -> str:
    client = _ensure_stripe()
    domain = _domain_url()
    success_url = success_url or f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = cancel_url or f"{domain}/cancel"
    try:
        session = client.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url
    except Exception as exc:  # pragma: no cover - network interaction
        _LOGGER.exception("Stripe checkout error: %s", exc)
        raise RuntimeError(f"Stripe error: {exc}") from exc


def create_subscription_session(
    price_id: str,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
) -> str:
    """Create a Stripe checkout session for subscriptions."""

    client = _ensure_stripe()
    domain = _domain_url()
    success_url = success_url or f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = cancel_url or f"{domain}/cancel"
    try:
        session = client.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url
    except Exception as exc:  # pragma: no cover - network interaction
        _LOGGER.exception("Stripe subscription error: %s", exc)
        raise RuntimeError(f"Stripe subscription error: {exc}") from exc


def create_refund(payment_intent: str) -> str:
    """Issue a refund for a given payment intent."""

    client = _ensure_stripe()
    try:
        refund = client.Refund.create(payment_intent=payment_intent)
        return refund.id
    except Exception as exc:  # pragma: no cover - network interaction
        _LOGGER.exception("Stripe refund error: %s", exc)
        raise RuntimeError(f"Stripe refund error: {exc}") from exc


def create_payout(amount: int, currency: str = "usd") -> str:
    """Create a payout to the connected account."""

    client = _ensure_stripe()
    try:
        payout = client.Payout.create(amount=amount, currency=currency)
        return payout.id
    except Exception as exc:  # pragma: no cover - network interaction
        _LOGGER.exception("Stripe payout error: %s", exc)
        raise RuntimeError(f"Stripe payout error: {exc}") from exc
