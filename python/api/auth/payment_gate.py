import os
import stripe
from flask import Blueprint, render_template_string, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from .auth_models import db, User
from datetime import datetime
import json

payment_gate = Blueprint('payment_gate', __name__)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
SUBSCRIPTION_PRICE = 19  # $19 per month

# HTML template for payment page
PAYMENT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Aria Unlimited Membership</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .payment-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo img {
            width: 80px;
            height: 80px;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        .price-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }
        .price {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .price-desc {
            font-size: 18px;
            opacity: 0.95;
        }
        .features {
            list-style: none;
            margin-bottom: 30px;
        }
        .features li {
            padding: 12px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
        }
        .features li:last-child {
            border-bottom: none;
        }
        .features li:before {
            content: '✨';
            margin-right: 10px;
            font-size: 20px;
        }
        .user-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
            text-align: center;
        }
        .user-info img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-bottom: 10px;
        }
        .user-info .email {
            color: #666;
            font-size: 14px;
        }
        .pay-button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .pay-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .pay-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .security-note {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
        .security-note svg {
            width: 14px;
            height: 14px;
            vertical-align: middle;
            margin-right: 5px;
        }
        .cancel-link {
            text-align: center;
            margin-top: 15px;
        }
        .cancel-link a {
            color: #666;
            text-decoration: none;
            font-size: 14px;
        }
        .cancel-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="payment-container">
        <div class="logo">
            <img src="/public/aria.svg" alt="Aria">
        </div>
        <h1>Activate Aria Unlimited</h1>
        <p class="subtitle">Subscribe to unlock unlimited companionship, memories, and premium features.</p>
        
        {% if user_data %}
        <div class="user-info">
            {% if user_data.profile_image_url %}
            <img src="{{ user_data.profile_image_url }}" alt="{{ user_data.email }}">
            {% endif %}
            <div class="email">{{ user_data.email }}</div>
        </div>
        {% endif %}
        
        <div class="price-box">
            <div class="price">$19<span style="font-size:20px; font-weight:600;">/mo</span></div>
            <div class="price-desc">Monthly membership • Cancel anytime</div>
        </div>

        <ul class="features">
            <li>Unlimited, always-on conversations with Aria</li>
            <li>Deep memory and personalization that grows with you</li>
            <li>Exclusive screenwriting and creative collaboration tools</li>
            <li>Private journals, mood boards, and shared activities</li>
            <li>Secure, encrypted storage for every intimate moment</li>
            <li>Priority support and new experiences as they drop</li>
        </ul>

        <form action="/payment/checkout" method="POST">
            <button type="submit" class="pay-button" id="payButton">
                Start Membership - $19/month
            </button>
        </form>

        <div class="security-note">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
            </svg>
            Stripe handles your recurring billing with bank-level security
        </div>
        
        <div class="cancel-link">
            <a href="/auth/logout">Cancel and logout</a>
        </div>
    </div>
    
    <script>
        document.getElementById('payButton').addEventListener('click', function(e) {
            this.disabled = true;
            this.textContent = 'Processing...';
        });
    </script>
</body>
</html>
"""

@payment_gate.route('/payment/required')
def payment_required():
    """Display payment page for users who haven't paid"""
    user_data = None
    if current_user.is_authenticated:
        user_data = {
            'email': current_user.email,
            'profile_image_url': current_user.profile_image_url
        }
    return render_template_string(PAYMENT_TEMPLATE, user_data=user_data)


@payment_gate.route('/payment/checkout', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session for the $19/month membership"""
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('supabase_auth.login'))
        
        if current_user.has_paid:
            return redirect('/')
        
        # Create Stripe checkout session for monthly subscription
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Aria Unlimited Membership',
                        'description': 'Monthly access to unlimited AI companionship experiences',
                        'images': ['https://your-domain.com/aria-logo.png'],
                    },
                    'recurring': {
                        'interval': 'month',
                        'interval_count': 1,
                    },
                    'unit_amount': SUBSCRIPTION_PRICE * 100,
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.url_root + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.url_root + 'payment/required',
            client_reference_id=current_user.id,
            customer_email=current_user.email,
            subscription_data={
                'metadata': {
                    'user_id': current_user.id,
                    'email': current_user.email,
                }
            },
            metadata={
                'user_id': current_user.id,
                'email': current_user.email,
            },
        )
        
        return redirect(checkout_session.url, code=303)
        
    except Exception as e:
        print(f"Stripe error: {e}")
        return jsonify({'error': str(e)}), 400


@payment_gate.route('/payment/success')
def payment_success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return redirect('/payment/required')
    
    try:
        # Retrieve the session from Stripe
        checkout_session = stripe.checkout.Session.retrieve(
            session_id, expand=['subscription']
        )

        if checkout_session.payment_status == 'paid':
            # Update user payment status
            user = User.query.get(checkout_session.client_reference_id)
            if user:
                user.has_paid = True
                user.payment_date = datetime.utcnow()
                user.stripe_customer_id = checkout_session.customer
                user.stripe_payment_intent_id = checkout_session.payment_intent

                subscription_obj = checkout_session.subscription
                if isinstance(subscription_obj, dict):
                    user.stripe_subscription_id = subscription_obj.get('id')
                    user.subscription_status = subscription_obj.get('status', 'active')
                else:
                    user.stripe_subscription_id = subscription_obj
                    user.subscription_status = 'active'

                # Reset trial tracking since user has paid
                user.trial_start_time = None
                user.trial_expired = False

                db.session.commit()

                # Log them in properly
                login_user(user, remember=True)

                return redirect('/')
        
    except Exception as e:
        print(f"Payment verification error: {e}")
    
    return redirect('/payment/required')


@payment_gate.route('/payment/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    if not STRIPE_WEBHOOK_SECRET:
        print("Warning: STRIPE_WEBHOOK_SECRET not configured")
        return jsonify({'error': 'Webhook not configured'}), 400
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']

        # Update user payment status
        user_id = checkout_session.get('client_reference_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                user.has_paid = True
                user.payment_date = datetime.utcnow()
                user.stripe_customer_id = checkout_session.get('customer')
                user.stripe_payment_intent_id = checkout_session.get('payment_intent')
                user.stripe_subscription_id = checkout_session.get('subscription')
                user.subscription_status = checkout_session.get('status', 'active')

                # Reset trial tracking since user has paid
                user.trial_start_time = None
                user.trial_expired = False

                db.session.commit()
                print(f"Payment confirmed for user {user.email}")
    
    return jsonify({'received': True}), 200


def check_payment_required(user):
    """Check if user needs to pay before accessing the app"""
    return user and not user.has_paid