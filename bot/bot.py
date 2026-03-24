"""
LMS Telegram Bot Entry Point

Supports --test mode for offline testing without Telegram connection.
Usage:
    uv run bot.py --test "/start"   # Prints response to stdout
    uv run bot.py --test "what labs are available"  # Natural language query
    uv run bot.py                   # Starts Telegram bot
"""

import asyncio
import sys
from handlers.start import handle_start, START_KEYBOARD
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.labs import handle_labs
from handlers.scores import handle_scores
from intent_router import route_intent
from config import settings


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
        # Telegram mode: start the aiogram bot
        print("Starting Telegram bot...")
        run_telegram_bot()


def run_telegram_bot():
    """Run the Telegram bot using aiogram."""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import CommandStart, Command
    
    # Check for bot token
    if not settings.bot_token:
        print("Error: BOT_TOKEN is not set. Please set BOT_TOKEN in .env.bot.secret")
        sys.exit(1)
    
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Handler for /start command
    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        response = handle_start()
        # Send with inline keyboard
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="📚 Available Labs", callback_data="cmd_labs"),
                    types.InlineKeyboardButton(text="🏥 Health Check", callback_data="cmd_health"),
                ],
                [
                    types.InlineKeyboardButton(text="📊 Lab Scores", callback_data="cmd_scores_lab04"),
                    types.InlineKeyboardButton(text="🏆 Top Learners", callback_data="cmd_top_learners"),
                ],
                [
                    types.InlineKeyboardButton(text="❓ Help", callback_data="cmd_help"),
                ],
            ]
        )
        await message.answer(response, reply_markup=keyboard)
    
    # Handler for /help command
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        response = handle_help()
        await message.answer(response)
    
    # Handler for /health command
    @dp.message(Command("health"))
    async def cmd_health(message: types.Message):
        response = handle_health()
        await message.answer(response)
    
    # Handler for /labs command
    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message):
        response = handle_labs()
        await message.answer(response)
    
    # Handler for /scores command
    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message):
        # Extract lab name from command args
        lab_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        response = handle_scores(lab_name)
        await message.answer(response)
    
    # Handler for callback queries (inline buttons)
    @dp.callback_query(lambda c: c.data.startswith("cmd_"))
    async def process_callback(callback: types.CallbackQuery):
        action = callback.data
        
        if action == "cmd_labs":
            response = handle_labs()
        elif action == "cmd_health":
            response = handle_health()
        elif action == "cmd_help":
            response = handle_help()
        elif action == "cmd_scores_lab04":
            response = handle_scores("lab-04")
        elif action == "cmd_top_learners":
            response = "Top learners feature coming soon! Try asking: 'who are the top 5 students in lab 4'"
        else:
            response = "Unknown action"
        
        await bot.answer_callback_query(callback.id)
        await bot.send_message(callback.from_user.id, response)
    
    # Handler for all other messages (natural language)
    @dp.message()
    async def handle_message(message: types.Message):
        text = message.text
        if not text:
            return
        
        # Route through intent router
        response = route_intent(text)
        await message.answer(response)
    
    # Start the bot
    print(f"Bot started. Polling for messages...")
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
