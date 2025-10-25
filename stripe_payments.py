import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required

stripe_payments = Blueprint('stripe_payments', __name__)

_stripe_initialized = False
_stripe_available = False


def init_stripe():
    global _stripe_initialized, _stripe_available
    
    if _stripe_initialized:
        return _stripe_available
    
    _stripe_initialized = True
    
    stripe_key = os.getenv('STRIPE_SECRET_KEY')
    if not stripe_key:
        print(
            "STRIPE_SECRET_KEY not found in environment. "
            "Payment features will be disabled. "
            "Add STRIPE_SECRET_KEY to your Replit Secrets to enable payments."
        )
        _stripe_available = False
        return False
    
    try:
        import stripe
        stripe.api_key = stripe_key
        _stripe_available = True
        print("Stripe initialized successfully")
        return True
    except ImportError:
        print("Stripe package not installed")
        _stripe_available = False
        return False
    except Exception as e:
        print(f"Error initializing Stripe: {str(e)}")
        _stripe_available = False
        return False


@stripe_payments.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    if not init_stripe():
        return jsonify({
            'error': 'Stripe is not configured. Please add STRIPE_SECRET_KEY to your environment.'
        }), 503
    
    try:
        import stripe
        
        data = request.get_json() or {}
        price_id = data.get('price_id', os.getenv('STRIPE_PRICE_ID', 'price_example'))
        
        dev_domain = os.getenv('REPLIT_DEV_DOMAIN', '')
        domains = os.getenv('REPLIT_DOMAINS', '')
        base_domain = dev_domain or domains.split(',')[0] if domains else ''
        
        if not base_domain:
            return jsonify({'error': 'Unable to determine domain for redirect URLs'}), 500
        
        success_url = f"https://{base_domain}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"https://{base_domain}/payment"
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        return jsonify({'checkout_url': checkout_session.url})
    
    except Exception as e:
        current_app.logger.error(f"Error creating checkout session: {str(e)}")
        return jsonify({'error': str(e)}), 500


@stripe_payments.route('/webhook', methods=['POST'])
def stripe_webhook():
    if not init_stripe():
        return jsonify({'error': 'Stripe not configured'}), 503
    
    try:
        import stripe
        
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        
        # SECURITY: Always require webhook secret for signature verification
        if not webhook_secret:
            current_app.logger.error(
                "STRIPE_WEBHOOK_SECRET is required for webhook security. "
                "Add it to your Replit Secrets to enable webhook processing."
            )
            return jsonify({
                'error': 'Webhook secret not configured. Cannot process webhooks securely.'
            }), 503
        
        if not sig_header:
            current_app.logger.warning("Webhook request missing Stripe-Signature header")
            return jsonify({'error': 'Missing signature header'}), 400
        
        # Verify webhook signature to prevent spoofing
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            current_app.logger.error(f"Invalid webhook payload: {str(e)}")
            return jsonify({'error': 'Invalid payload'}), 400
        except stripe.error.SignatureVerificationError as e:
            current_app.logger.error(f"Webhook signature verification failed: {str(e)}")
            return jsonify({'error': 'Invalid signature'}), 400
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            current_app.logger.info(f"Payment successful for session {session['id']}")
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        current_app.logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500


def init_stripe_routes(app):
    app.register_blueprint(stripe_payments)
    init_stripe()
    print("Stripe payment routes registered")
