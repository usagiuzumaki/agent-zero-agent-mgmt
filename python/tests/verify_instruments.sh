#!/bin/bash
set -e

echo "Starting E-girl Instruments Verification..."

# Run tests for each instrument
echo "1. Testing E-girl Tool Wrapper (egirl_tool.py)..."
python -m pytest python/tests/test_egirl_tool.py -v

echo "2. Testing Stripe Integration (stripe.py)..."
python -m pytest python/tests/test_stripe_integration.py -v

echo "3. Testing ElevenLabs Integration (elevenlabs.py)..."
python -m pytest python/tests/test_elevenlabs.py -v

echo "4. Testing Stable Diffusion Integration (stable_diffusion.py)..."
python -m pytest python/tests/test_stable_diffusion.py -v

echo "5. Testing Instagram Integration (instagram.py)..."
python -m pytest python/tests/test_instagram_integration.py -v

echo "6. Testing Video Generation (video.py)..."
python -m pytest python/tests/test_video_generation.py -v

echo "All verifications passed successfully!"
