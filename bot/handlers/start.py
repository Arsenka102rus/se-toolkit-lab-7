"""Handler for /start command."""

# Inline keyboard buttons for common actions
START_KEYBOARD = {
    "inline_keyboard": [
        [
            {"text": "📚 Available Labs", "callback_data": "cmd_labs"},
            {"text": "🏥 Health Check", "callback_data": "cmd_health"},
        ],
        [
            {"text": "📊 Lab Scores", "callback_data": "cmd_scores_lab04"},
            {"text": "🏆 Top Learners", "callback_data": "cmd_top_learners"},
        ],
        [
            {"text": "❓ Help", "callback_data": "cmd_help"},
        ],
    ]
}


def handle_start() -> str:
    """Handle the /start command.
    
    Returns:
        Welcome message for new users.
    """
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you interact with the LMS backend through chat.\n\n"
        "Use the buttons below or type commands:\n"
        "/start - Welcome message\n"
        "/help - List all commands\n"
        "/health - Check system status\n"
        "/labs - Browse available labs\n"
        "/scores <lab> - View task pass rates\n\n"
        "Or ask in plain language:\n"
        "• \"What labs are available?\"\n"
        "• \"Show me scores for lab 4\"\n"
        "• \"Which lab has the lowest pass rate?\""
    )
