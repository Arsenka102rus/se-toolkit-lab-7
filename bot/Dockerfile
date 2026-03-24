# Bot container for LMS Telegram Bot
# Uses uv for dependency management (no requirements.txt)

FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy bot project files
COPY bot/pyproject.toml bot/uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy bot source code
COPY bot/ ./bot/

# Copy root .env.bot.secret for environment variables
# (Will be overridden by docker-compose environment)
COPY .env.bot.example .env.bot.secret

# Set Python path to find bot module
ENV PYTHONPATH=/app

# Run the bot
CMD ["uv", "run", "python", "-m", "bot.bot"]
