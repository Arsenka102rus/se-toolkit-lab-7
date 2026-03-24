"""Handler for /start command."""


def handle_start() -> str:
    """Handle the /start command.
    
    Returns:
        Welcome message for new users.
    """
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you interact with the LMS backend through chat.\n\n"
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - List all commands\n"
        "/health - Check system status\n"
        "/labs - Browse available labs\n"
        "/scores <lab> - View task pass rates\n\n"
        "You can also ask questions in plain language!"
    )
