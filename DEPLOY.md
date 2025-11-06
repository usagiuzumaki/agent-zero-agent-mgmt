# 🚀 Agent Zero (Aria) - Production Deployment Guide

## Overview
Agent Zero (Aria) is a production-ready AI assistant with personality features, image generation, and payment processing capabilities.

## ✅ Pre-Deployment Checklist

### Required Environment Variables
Set these in Replit Secrets panel:

**REQUIRED:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `DATABASE_URL` - PostgreSQL connection (auto-configured by Replit)
- `FLASK_SECRET_KEY` - Session secret (auto-generated if not set)

**OPTIONAL (but recommended):**
- `REPLICATE_API_TOKEN` - For image generation
- `STRIPE_SECRET_KEY` - For payment processing
- `STRIPE_WEBHOOK_SECRET` - For secure webhook handling
- `ANTHROPIC_API_KEY` - For Claude models
- `GOOGLE_API_KEY` - For Gemini models

## 📦 Quick Deployment Steps

### 1. Set Up Secrets
```bash
# In Replit Secrets panel, add:
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
STRIPE_SECRET_KEY=sk_test_...
```

### 2. Install Production Dependencies
```bash
# Use optimized production requirements
pip install -r requirements_production.txt
```

### 3. Run Database Migrations
```bash
python scripts/migrate.py
```

### 4. Start Production Server
```bash
# Production mode with gunicorn
bash scripts/start_production.sh

# OR directly with Python
python run_ui.py --host=0.0.0.0 --port=${PORT:-5000}
```

## 🔍 Health Monitoring

### Health Check Endpoints
- **GET /healthz** - Basic health check
- **GET /api/health** - Detailed health status with database check

```bash
# Test health endpoint
curl http://localhost:5000/healthz
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Agent Zero (Aria)",
  "timestamp": "2024-11-06 00:00:00 UTC",
  "port": 5000,
  "environment": "production",
  "database": "connected"
}
```

## 🚀 Replit Deployment Configuration

### Deployment Type: VM
The application is configured for **VM deployment** (always running) because it:
- Maintains persistent agent memory
- Manages scheduled tasks
- Handles real-time conversations
- Processes payments and webhooks

### Deploy via Replit UI
1. Click **"Publish"** in the workspace header
2. Select **"VM"** deployment type
3. Configure secrets in the deployment panel
4. Click **"Deploy"**

### Deployment Settings (Already Configured)
- **Entry Point:** `run_ui.py`
- **Port Binding:** Uses `$PORT` environment variable
- **Run Command:** `python run_ui.py --host=0.0.0.0 --port=5000`

## 📊 Production Features

### Database
- Auto-connects to Replit PostgreSQL
- Automatic migration on startup
- User authentication tables
- OAuth token management

### Performance Optimizations
- Gunicorn production server (when available)
- Optimized dependencies (no heavy ML libraries unless needed)
- Efficient error handling
- Request logging suppression

### Security
- CSRF protection
- Session management
- API key authentication
- Stripe webhook signature verification

## 🔧 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Kill existing process
pkill -f "python run_ui.py"
# Restart
bash scripts/start_production.sh
```

**Database Connection Failed:**
```bash
# Check PostgreSQL status
echo $DATABASE_URL
# Re-run migrations
python scripts/migrate.py
```

**Missing Dependencies:**
```bash
# Install production requirements
pip install -r requirements_production.txt
```

## 📈 Monitoring

### Application Logs
```bash
# View real-time logs
tail -f logs/*.log
```

### Performance Metrics
- Monitor `/healthz` endpoint response time
- Check memory usage: `ps aux | grep python`
- Database connections: Check pool status

## 🎯 Production Best Practices

1. **Always use environment variables** for sensitive data
2. **Run migrations** before each deployment
3. **Monitor health endpoints** regularly
4. **Keep logs** for debugging
5. **Use production requirements** file for optimal performance
6. **Enable HTTPS** via Replit's automatic SSL
7. **Set up alerts** for health check failures

## 🆘 Support

For deployment issues:
1. Check health endpoint: `/healthz`
2. Review logs in `logs/` directory
3. Verify environment variables are set
4. Ensure database is connected
5. Check Replit deployment logs

## 📝 Quick Commands Reference

```bash
# Run migrations
python scripts/migrate.py

# Start production server
bash scripts/start_production.sh

# Check health
curl http://localhost:5000/healthz

# View logs
tail -f logs/*.log

# Install dependencies
pip install -r requirements_production.txt
```

---

**Ready for Production!** Your Agent Zero (Aria) is configured for reliable, scalable deployment on Replit. 🚀