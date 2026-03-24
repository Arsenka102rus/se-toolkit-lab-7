# Bot container for LMS Telegram Bot
# Uses uv for dependency management (no requirements.txt)

FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy bot project files
COPY bot/pyproject.toml ./

# Install dependencies using uv (generates uv.lock automatically)
RUN uv sync --no-dev

# Copy bot source code
COPY bot/ ./bot/

# Copy root .env.bot.example as placeholder
COPY .env.bot.example .env.bot.secret

# Set Python path to find bot module
ENV PYTHONPATH=/app

# Run the bot
CMD ["uv", "run", "python", "-m", "bot.bot"]
