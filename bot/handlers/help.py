"""Handler for /help command."""


def handle_help() -> str:
    """Handle the /help command.
    
    Returns:
        List of available commands.
    """
    return (
        "📖 Available Commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check backend system status\n"
        "/labs - Browse available labs\n"
        "/scores <lab> - View pass rates for a specific lab\n\n"
        "You can also ask questions in plain language like:\n"
        "• What labs are available?\n"
        "• Show me my scores for lab-01\n"
        "• Is the system working?"
    )
