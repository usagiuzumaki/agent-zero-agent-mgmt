import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add repo root to path
sys.path.append(os.getcwd())

# Mock dependencies BEFORE importing the module under test
sys.modules['stripe'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['python.helpers.dotenv'] = MagicMock()

from python.helpers.egirl import stripe

class TestStripeIntegration(unittest.TestCase):

    def setUp(self):
        # Reset the mock stripe module before each test
        sys.modules['stripe'].reset_mock()
        # Reset the _STRIPE_INITIALISED flag to force re-initialization logic if needed
        stripe._STRIPE_INITIALISED = False
        stripe.stripe = sys.modules['stripe']

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    @patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_123", "DOMAIN_URL": "http://test.com"})
    def test_create_checkout_session_success(self, mock_install):
        # Setup Mock
        mock_stripe = sys.modules['stripe']
        mock_session = MagicMock()
        mock_session.url = "http://test.com/checkout"
        mock_stripe.checkout.Session.create.return_value = mock_session

        # Execute
        url = stripe.create_checkout_session("price_123")

        # Verify
        self.assertEqual(url, "http://test.com/checkout")
        mock_stripe.checkout.Session.create.assert_called_once()
        args, kwargs = mock_stripe.checkout.Session.create.call_args
        self.assertEqual(kwargs['mode'], 'payment')
        self.assertEqual(kwargs['line_items'], [{"price": "price_123", "quantity": 1}])
        self.assertEqual(kwargs['success_url'], "http://test.com/success?session_id={CHECKOUT_SESSION_ID}")
        self.assertEqual(kwargs['cancel_url'], "http://test.com/cancel")

        # Verify API key was set
        self.assertEqual(mock_stripe.api_key, "sk_test_123")

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    @patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_123"})
    def test_create_subscription_session_success(self, mock_install):
        # Setup Mock
        mock_stripe = sys.modules['stripe']
        mock_session = MagicMock()
        mock_session.url = "http://test.com/sub"
        mock_stripe.checkout.Session.create.return_value = mock_session

        # Execute
        url = stripe.create_subscription_session("price_sub")

        # Verify
        self.assertEqual(url, "http://test.com/sub")
        mock_stripe.checkout.Session.create.assert_called_once()
        args, kwargs = mock_stripe.checkout.Session.create.call_args
        self.assertEqual(kwargs['mode'], 'subscription')

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    @patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_123"})
    def test_create_refund_success(self, mock_install):
        # Setup Mock
        mock_stripe = sys.modules['stripe']
        mock_refund = MagicMock()
        mock_refund.id = "re_123"
        mock_stripe.Refund.create.return_value = mock_refund

        # Execute
        refund_id = stripe.create_refund("pi_123")

        # Verify
        self.assertEqual(refund_id, "re_123")
        mock_stripe.Refund.create.assert_called_once_with(payment_intent="pi_123")

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    @patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_123"})
    def test_create_payout_success(self, mock_install):
        # Setup Mock
        mock_stripe = sys.modules['stripe']
        mock_payout = MagicMock()
        mock_payout.id = "po_123"
        mock_stripe.Payout.create.return_value = mock_payout

        # Execute
        payout_id = stripe.create_payout(1000)

        # Verify
        self.assertEqual(payout_id, "po_123")
        mock_stripe.Payout.create.assert_called_once_with(amount=1000, currency="usd")

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    def test_missing_api_key(self, mock_install):
        # Ensure env var is missing
        with patch.dict(os.environ, {}, clear=True):
             with self.assertRaises(RuntimeError) as context:
                stripe.create_checkout_session("price_123")
             self.assertIn("STRIPE_SECRET_KEY is not configured", str(context.exception))

    @patch('python.helpers.egirl.stripe._install_stripe_package')
    @patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_123"})
    def test_stripe_api_error(self, mock_install):
        # Setup Mock to raise exception
        mock_stripe = sys.modules['stripe']
        mock_stripe.checkout.Session.create.side_effect = Exception("API Error")

        # Execute & Verify
        with self.assertRaises(RuntimeError) as context:
            stripe.create_checkout_session("price_123")
        self.assertIn("Stripe error: API Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
