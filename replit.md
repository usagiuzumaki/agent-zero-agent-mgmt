# Agent Zero on Replit

## Project Overview

Agent Zero is a personal, organic agentic AI framework that grows and learns with you. This is a fully functional web-based AI assistant that can:

- Execute code and terminal commands
- Search the web
- Manage persistent memory
- Create and manage subordinate agents for complex tasks
- Integrate with multiple LLM providers (OpenAI, Anthropic, Ollama, etc.)
- **Generate images with Stable Diffusion** via Replicate API
- **User authentication** with Replit Auth (Google, GitHub, email/password)
- **Payment processing** with Stripe integration

## Current State

**Status:** ✅ Fully functional web UI running on port 5000

The application is successfully running with:
- Flask web server on 0.0.0.0:5000
- Web-based chat interface
- Multi-agent system support
- Extensible tool and prompt system
- PostgreSQL database for user management
- Stripe payment checkout integration
- Replit Auth for secure authentication
- Replicate API for AI image generation

## Setup Notes

### Dependencies

Due to Replit's disk space limitations, we installed only essential dependencies:
- Core web framework: Flask, FastAPI, a2wsgi
- LLM providers: LiteLLM, OpenAI SDK, Anthropic, LangChain
- Essential utilities: GitPython, docker client, psutil, diskcache
- Payment & Auth: Stripe, Flask-Login, Flask-Dance, Flask-SQLAlchemy, PyJWT
- Image generation: Replicate SDK

**Heavy ML libraries NOT installed** (optional features):
- sentence-transformers (local embeddings)
- torch, transformers (ML models)
- faiss-cpu (vector search)
- playwright (browser automation)
- gradio, accelerate, diffusers (local image generation)

**Image Generation via Replicate API**: Instead of installing heavy local models (torch, diffusers, etc.), we use the Replicate API for Stable Diffusion image generation. This saves ~5GB of disk space and provides faster, higher-quality results at approximately $0.01 per image.

These optional features will gracefully degrade if users try to use them without the dependencies.

### Code Modifications

**models.py**: Made `sentence_transformers` import lazy to avoid blocking at module load time. The import now happens inside `LocalSentenceTransformerWrapper.__init__()` only when actually needed.

**python/helpers/stable_diffusion.py**: Created API-based Stable Diffusion wrapper that uses Replicate API when `REPLICATE_API_TOKEN` is available. Note: Local generation fallback is not available on Replit due to missing heavy ML dependencies (torch, diffusers).

**Database**: Added PostgreSQL database with User and OAuth models for authentication. Database auto-initializes on startup using pg8000 driver.

## Configuration

### API Keys & Secrets

Agent Zero requires various API keys and secrets. Configure them using Replit Secrets:

**Core LLM Providers:**
- `OPENAI_API_KEY` - For OpenAI models (GPT-4, GPT-3.5, etc.)
- `ANTHROPIC_API_KEY` - For Claude models
- Other provider keys as needed

**Image Generation:**
- `REPLICATE_API_TOKEN` - For Stable Diffusion image generation via Replicate API

**Payment Processing (Optional):**
- `STRIPE_SECRET_KEY` - Stripe secret key (starts with `sk_test_` or `sk_live_`)
- `STRIPE_WEBHOOK_SECRET` - Required for secure webhook signature verification (starts with `whsec_`)
- `STRIPE_PRICE_ID` - (Optional) Default price ID for checkout sessions

**Database & Sessions:**
- `DATABASE_URL` - Auto-configured by Replit PostgreSQL
- `SESSION_SECRET` - Auto-configured by Replit for secure session management

The application will automatically create a `.env` file and manage secrets. An RFC password is auto-generated for remote function calls.

### Stripe Setup (Optional)

To enable Stripe payments:

1. **Get your API keys** from [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
   - Add `STRIPE_SECRET_KEY` to Replit Secrets (starts with `sk_test_` or `sk_live_`)

2. **Configure webhooks** in [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks)
   - Webhook URL: `https://your-replit-url.replit.dev/webhook`
   - Events to listen for: `checkout.session.completed`
   - Copy the webhook signing secret and add as `STRIPE_WEBHOOK_SECRET` to Replit Secrets

3. **Create a product and price** in Stripe Dashboard
   - Optional: Add the price ID as `STRIPE_PRICE_ID` to Replit Secrets

4. **Test with Stripe CLI** (recommended):
   ```bash
   stripe listen --forward-to localhost:5000/webhook
   stripe trigger checkout.session.completed
   ```

**Security Note**: The webhook handler requires `STRIPE_WEBHOOK_SECRET` to verify webhook signatures and prevent payment spoofing attacks. Without it, webhook processing is disabled for security.

### Replit Auth Setup (Optional)

Replit Auth is automatically configured and works out-of-the-box:

- **No manual setup required** - The integration uses your Repl's ID for authentication
- **Auto-configured secrets**: `SESSION_SECRET` is managed by Replit
- **Supported login methods**: Google, GitHub, X (Twitter), Apple, email/password
- **Auth routes**: `/auth/login`, `/auth/logout`, `/auth/callback`

Users can sign in at `/login` and access protected routes like `/dashboard` and `/payment`.

### Image Generation Setup

Agent Zero uses Replicate API for Stable Diffusion image generation:

- **Add `REPLICATE_API_TOKEN`** from [Replicate.com](https://replicate.com/account/api-tokens)
- **Cost**: ~$0.01 per image
- **Fallback**: Local generation is NOT available on Replit (requires ~5GB of dependencies)
- **Alternative**: Configure a different image generation API if preferred

### Settings

Access settings via the gear icon in the web UI to configure:
- **Chat Model**: Primary LLM for conversations (default: OpenAI)
- **Utility Model**: Smaller model for internal tasks
- **Embedding Model**: For memory and knowledge retrieval
- **Agent Profile**: Customize agent behavior with different prompt sets
- **Memory & Knowledge**: Configure persistent storage locations

## Project Structure

```
/agents/          - Agent implementations and specialized agents
/prompts/         - System prompts and behavior templates
/python/          - Core Python helpers and API handlers
  /api/          - REST API endpoints
  /helpers/      - Utility modules (includes stable_diffusion.py)
  /tools/        - Default agent tools
/webui/          - Frontend web interface (includes auth pages)
/knowledge/      - Knowledge base documents
/memory/         - Persistent agent memory
/instruments/    - Custom tools and procedures
/work_dir/       - Agent working directory
initialize.py    - Initialization and configuration
models.py        - LLM model wrappers
run_ui.py        - Web server entry point
auth_models.py   - PostgreSQL User and OAuth models
replit_auth.py   - Replit Auth OpenID Connect integration
stripe_payments.py - Stripe payment routes and webhook handling
```

## Architecture

- **Multi-Agent System**: Each agent can spawn subordinate agents for subtasks
- **Memory System**: Persistent memory with automatic consolidation
- **Tool System**: Extensible tools for code execution, web search, image generation, etc.
- **Prompt System**: Fully customizable via markdown files in /prompts/
- **Extension System**: Hook into agent lifecycle events
- **Authentication**: Replit Auth with OpenID Connect (supports Google, GitHub, email/password)
- **Database**: PostgreSQL for user management and OAuth token storage
- **Payments**: Stripe Checkout with secure webhook verification

## Usage

1. **Start the Application**: The workflow automatically runs the web UI on port 5000
2. **Configure API Keys**: Add your LLM provider keys in settings or Replit Secrets
3. **Authentication** (Optional):
   - Visit `/login` to sign in with Replit Auth
   - Access protected routes like `/dashboard` and `/payment`
   - Logout via `/auth/logout`
4. **Start Chatting**: Use the chat interface to interact with Agent Zero
5. **Generate Images**: Ask Agent Zero to generate images (uses Replicate API)
6. **Payment Processing** (Optional):
   - Configure STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET
   - Use `/create-checkout-session` for payments
7. **Advanced Features**: 
   - Load/Save chats for persistence
   - Create scheduled tasks
   - Manage agent behaviors
   - Import knowledge documents

## Code Execution & Package Installation Capabilities

### Enhanced Code Execution System
Agent Zero (Aria) now has improved code execution capabilities that work reliably in Replit's deployed environment:

1. **DeploymentCodeRunner**: Custom code runner that avoids sandboxing issues
   - Executes Python code in isolated subprocesses with timeouts
   - Runs shell commands safely without hanging
   - Tests package imports before using them

2. **Direct Package Installation**: New tools bypass sandboxing limitations
   - `PackageInstaller`: Install/uninstall Python packages directly
   - `SystemCommand`: Execute system commands without session hanging
   - `EnhancedCodeExecution`: Improved code execution for deployed environments

3. **API-Based Workarounds**: For problematic packages like `replicate`
   - Direct HTTP endpoints bypass sandboxed execution
   - Image generation via `/api/generate-image` endpoint
   - Works reliably without import hanging issues

### When Deployed, Agent Zero Can:
✅ Install Python packages via pip  
✅ Execute Python code and shell commands  
✅ Access external APIs and services  
✅ Manage files and directories  
✅ Generate images via Replicate API  
✅ Process payments via Stripe  
✅ Authenticate users via Replit Auth

### Deployment Environment Notes:
- **No Docker Support**: Replit doesn't allow nested virtualization
- **Local Execution Only**: Code runs in subprocess, not containers
- **API Workarounds Available**: For packages that hang in sandboxed execution
- **Full pip Access**: Can install most Python packages at runtime

## Known Limitations on Replit

1. **Local Embeddings**: sentence-transformers not installed - use OpenAI embeddings instead
2. **Browser Automation**: Playwright not available - web scraping features limited
3. **Local Image Generation**: Heavy ML dependencies not installed - use Replicate API instead (enabled by default)
4. **TTS/STT**: Whisper and Kokoro models will show errors but won't break the app
5. **Docker Execution**: Not available - use LocalInteractiveSession or enhanced tools instead

## Deployment

The application is configured for VM deployment (always running) since it maintains:
- Persistent memory and state
- Background job scheduling
- Real-time agent operations

## Troubleshooting

### API Key Errors
If you see API key errors, configure them in Settings or via Replit Secrets.

### Memory/Embedding Errors
If using local embeddings fails, switch to OpenAI embeddings in Settings → Embedding Model.

### Import Errors
Most heavy ML dependencies are optional. The app will continue to work with core features.

## Recent Changes

- **2025-11-06**: Personalized Welcome Messages & Activities Menu
  - **Dynamic Welcome System**: Replaced generic "Agent Zero" with personalized "Aria" greetings
  - Created `python/helpers/aria_welcome.py` for dynamic, time-based welcome messages
  - Welcome messages now change based on time of day, weekday, and randomized personality
  - Updated agent name from "A0" to "Aria" throughout the interface
  - **Activities Dropdown Menu**: Created interactive activities dropdown menu in chat interface
  - Added 8 interactive activities including personality quiz, mood sharing, story creation
  - Integrated with Aria's personality features (python/helpers/aria_personality.py)
  - Added custom CSS for dark theme styling
  - Activities automatically populate chat input with contextual prompts

- **2025-10-25**: Added Stripe payments, authentication, and Replicate image generation
  - Integrated Replicate API for Stable Diffusion image generation (~$0.01/image)
  - Added PostgreSQL database for user management
  - Integrated Replit Auth (Google, GitHub, email/password login)
  - Added Stripe payment processing with secure webhook verification
  - Created auth pages: /login, /dashboard, /payment
  - Fixed zstandard.backend_c import error from Python version mismatch
  - Installed: stripe, flask-dance, flask-login, flask-sqlalchemy, pyjwt, pg8000, replicate

- **2025-10-23**: Initial Replit setup
  - Installed minimal dependency set for disk space
  - Made sentence_transformers import lazy
  - Configured Flask for port 5000
  - Set up VM deployment

## Resources

- [Official Documentation](https://github.com/agent0ai/agent-zero)
- [Installation Guide](./docs/installation.md)
- [Usage Guide](./docs/usage.md)
- [Architecture](./docs/architecture.md)
