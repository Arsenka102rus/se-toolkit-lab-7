# LMS Telegram Bot — Development Plan

## Overview

This document outlines the implementation plan for building a Telegram bot that lets users interact with the LMS backend through chat. The bot supports slash commands like `/health`, `/labs`, and `/scores`, as well as natural language queries powered by an LLM.

## Architecture

### Handler Layer (`bot/handlers/`)

Handlers are pure functions that take input and return text. They don't depend on Telegram — the same logic works from `--test` mode, unit tests, or the actual Telegram bot. This is **separation of concerns**: business logic is isolated from the transport layer.

- `start.py` — Welcome message for `/start`
- `help.py` — Command list for `/help`
- `health.py` — Backend health check for `/health`
- `labs.py` — List available labs for `/labs`
- `scores.py` — Task pass rates for `/scores`

### Services Layer (`bot/services/`)

Services handle external dependencies:

- `lms_client.py` — HTTP client for the LMS backend API
- `llm_client.py` — Client for the LLM API (Task 3)

### Entry Point (`bot/bot.py`)

The entry point supports two modes:

1. **`--test` mode**: Reads a command from arguments, calls handlers directly, prints response to stdout. Used for offline testing without Telegram.
2. **Telegram mode**: Starts the aiogram bot, connects handlers to Telegram updates.

### Configuration (`bot/config.py`)

Uses `pydantic-settings` to load environment variables from `.env.bot.secret`. This keeps secrets out of code and provides type-safe configuration.

## Task Breakdown

### Task 1: Plan and Scaffold (P0)

**Goal:** Create project structure with testable handlers and `--test` mode.

- [x] Create `bot/` directory structure
- [x] Create `bot.py` with `--test` mode
- [x] Create placeholder handlers (`/start`, `/help`, `/health`, `/labs`, `/scores`)
- [x] Create `config.py` for environment loading
- [x] Create `pyproject.toml` with dependencies
- [ ] Write this `PLAN.md`

**Acceptance:** `uv run bot.py --test "/start"` prints welcome message and exits 0.

### Task 2: Backend Integration (P0)

**Goal:** Connect handlers to the LMS backend API.

- Create `services/lms_client.py` with Bearer token authentication
- Update `/health` to call `GET /health` on backend
- Update `/labs` to call `GET /items` and format results
- Update `/scores` to call `GET /analytics` with lab filter
- Add error handling for backend downtime

**Acceptance:** Commands return real data from backend. Backend down produces friendly message.

### Task 3: Intent-Based Natural Language Routing (P1)

**Goal:** Let users ask questions in plain language using an LLM.

- Create `services/llm_client.py` for LLM API calls
- Create `bot/intent_router.py` that sends user input to LLM with tool descriptions
- Wrap all 9 backend endpoints as LLM tools
- LLM decides which tool to call based on user intent

**Key insight:** The LLM reads tool descriptions to decide which to call. Description quality matters more than prompt engineering. Don't use regex to route — trust the LLM and improve descriptions if it picks wrong tools.

**Acceptance:** "what labs are available" returns the same data as `/labs`.

### Task 4: Containerize and Document (P3)

**Goal:** Deploy the bot alongside the backend on the VM.

- Create `bot/Dockerfile` for the bot container
- Add bot service to `docker-compose.yml`
- Configure container networking (use service names, not `localhost`)
- Update README with deployment instructions

**Acceptance:** Bot runs in Docker, responds in Telegram.

## Environment Variables

The bot requires `.env.bot.secret`:

```
BOT_TOKEN=<telegram-bot-token>
LMS_API_BASE_URL=http://backend:8000
LMS_API_KEY=my-secret-api-key
LLM_API_BASE_URL=http://llm:8080
LLM_API_KEY=<llm-api-key>
LLM_API_MODEL=coder-model
```

In Docker, URLs use service names (`backend`, `llm`) instead of `localhost`.

## Testing Strategy

1. **Unit tests**: Call handlers directly with known inputs
2. **Test mode**: `uv run bot.py --test "/command"` for manual testing
3. **Integration tests**: Run bot in Docker, send Telegram messages

## Deployment Flow

1. Build: `docker-compose build`
2. Start: `docker-compose up -d`
3. Check logs: `docker-compose logs -f bot`
4. Test in Telegram: Send `/start`
