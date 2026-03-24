"""
LMS Telegram Bot Entry Point

Supports --test mode for offline testing without Telegram connection.
Usage:
    uv run bot.py --test "/start"   # Prints response to stdout
    uv run bot.py --test "what labs are available"  # Natural language query
    uv run bot.py                   # Starts Telegram bot
"""

import sys
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.labs import handle_labs
from handlers.scores import handle_scores
from intent_router import route_intent


def handle_command(command: str) -> str:
    """
    Route a command string to the appropriate handler.
    
    Args:
        command: The command text (e.g., "/start", "/help", "/health")
    
    Returns:
        Response text to display
    """
    if command == "/start":
        return handle_start()
    elif command == "/help":
        return handle_help()
    elif command == "/health":
        return handle_health()
    elif command == "/labs":
        return handle_labs()
    elif command.startswith("/scores"):
        # Extract lab name if provided: /scores lab-01
        parts = command.split(maxsplit=1)
        lab_name = parts[1] if len(parts) > 1 else None
        return handle_scores(lab_name)
    else:
        return f"Unknown command: {command}. Use /help to see available commands."


def is_natural_language(message: str) -> bool:
    """Check if a message is natural language (not a slash command)."""
    return not message.startswith("/")


def main():
    """Main entry point with --test mode support."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode: read command from argument, print response to stdout
        if len(sys.argv) < 3:
            print("Usage: uv run bot.py --test <command>")
            print("Example: uv run bot.py --test \"/start\"")
            print("Example: uv run bot.py --test \"what labs are available\"")
            sys.exit(1)
        
        message = sys.argv[2]
        
        # Route to intent router for natural language, or command handler for slash commands
        if is_natural_language(message):
            response = route_intent(message)
        else:
            response = handle_command(message)
        
        print(response)
        sys.exit(0)
    else:
        # Telegram mode: start the bot
        print("Starting Telegram bot...")
        print("Telegram mode not yet implemented. Use --test mode for now.")
        print("Example: uv run bot.py --test \"what labs are available\"")
        sys.exit(0)


if __name__ == "__main__":
    main()
