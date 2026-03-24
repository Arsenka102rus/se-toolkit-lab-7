"""Handler for /health command."""

from services.lms_client import lms_client, BackendError


def handle_health() -> str:
    """Handle the /health command.
    
    Returns:
        Backend health status.
    """
    try:
        items = lms_client.get_items()
        if items is not None:
            item_count = len(items)
            return f"✅ Backend is healthy. {item_count} items available."
        else:
            return "⚠️ Backend returned empty response."
    except BackendError as e:
        return f"❌ Backend error: {str(e)}"
