# Agent Zero on Replit

## Project Overview

Agent Zero is a personal, organic agentic AI framework that grows and learns with you. This is a fully functional web-based AI assistant that can:

- Execute code and terminal commands
- Search the web
- Manage persistent memory
- Create and manage subordinate agents for complex tasks
- Integrate with multiple LLM providers (OpenAI, Anthropic, Ollama, etc.)

## Current State

**Status:** ✅ Fully functional web UI running on port 5000

The application is successfully running with:
- Flask web server on 0.0.0.0:5000
- Web-based chat interface
- Multi-agent system support
- Extensible tool and prompt system

## Setup Notes

### Dependencies

Due to Replit's disk space limitations, we installed only essential dependencies:
- Core web framework: Flask, FastAPI, a2wsgi
- LLM providers: LiteLLM, OpenAI SDK, Anthropic, LangChain
- Essential utilities: GitPython, docker client, psutil, diskcache

**Heavy ML libraries NOT installed** (optional features):
- sentence-transformers (local embeddings)
- torch, transformers (ML models)
- faiss-cpu (vector search)
- playwright (browser automation)
- gradio, accelerate, diffusers (image generation)

These features will gracefully degrade if users try to use them without the dependencies.

### Code Modifications

**models.py**: Made `sentence_transformers` import lazy to avoid blocking at module load time. The import now happens inside `LocalSentenceTransformerWrapper.__init__()` only when actually needed.

## Configuration

### API Keys

Agent Zero supports multiple LLM providers. Configure your API keys using Replit Secrets:
- `OPENAI_API_KEY` - For OpenAI models
- `ANTHROPIC_API_KEY` - For Claude models
- Other provider keys as needed

The application will automatically create a `.env` file and manage secrets. An RFC password is auto-generated for remote function calls.

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
  /helpers/      - Utility modules
  /tools/        - Default agent tools
/webui/          - Frontend web interface
/knowledge/      - Knowledge base documents
/memory/         - Persistent agent memory
/instruments/    - Custom tools and procedures
/work_dir/       - Agent working directory
initialize.py    - Initialization and configuration
models.py        - LLM model wrappers
run_ui.py        - Web server entry point
```

## Architecture

- **Multi-Agent System**: Each agent can spawn subordinate agents for subtasks
- **Memory System**: Persistent memory with automatic consolidation
- **Tool System**: Extensible tools for code execution, web search, etc.
- **Prompt System**: Fully customizable via markdown files in /prompts/
- **Extension System**: Hook into agent lifecycle events

## Usage

1. **Start the Application**: The workflow automatically runs the web UI on port 5000
2. **Configure API Keys**: Add your LLM provider keys in settings
3. **Start Chatting**: Use the chat interface to interact with Agent Zero
4. **Advanced Features**: 
   - Load/Save chats for persistence
   - Create scheduled tasks
   - Manage agent behaviors
   - Import knowledge documents

## Stable Diffusion Image Generation

**Status:** ✅ Fully functional via Replicate API

Agent Zero now supports Stable Diffusion image generation through the Replicate API, which provides cloud-based image generation without requiring heavy ML dependencies.

### Setup
1. Get a free API token from https://replicate.com/account/api-tokens
2. Add the token to Replit Secrets as `REPLICATE_API_TOKEN`
3. Agent Zero will automatically use the Replicate API for image generation

### Pricing
- Approximately $0.01 per image generation (SDXL model)
- Pay-as-you-go, no monthly fees
- Very affordable for testing and production use

### Configuration
You can customize the Stable Diffusion model by setting environment variables:
- `REPLICATE_SD_MODEL`: Model to use (default: `stability-ai/sdxl:latest`)
- Supports all Stable Diffusion models available on Replicate

## Known Limitations on Replit

1. **Local Embeddings**: sentence-transformers not installed - use OpenAI embeddings instead
2. **Browser Automation**: Playwright not available - web scraping features limited
3. **TTS/STT**: Whisper and Kokoro models will show errors but won't break the app
4. **Docker Execution**: Code execution runs locally, not in Docker container

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

- **2025-10-23**: Stable Diffusion Integration
  - Added Replicate API integration for image generation
  - Installed replicate Python SDK
  - Modified `python/helpers/stable_diffusion.py` to support both local and API-based generation
  - Configured REPLICATE_API_TOKEN secret
  
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
