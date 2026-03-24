"""Handler for /labs command."""

from services.lms_client import lms_client, BackendError


def handle_labs() -> str:
    """Handle the /labs command.
    
    Returns:
        List of available labs.
    """
    try:
        items = lms_client.get_items()
        if items is None:
            return "⚠️ No labs available (empty response from backend)."
        
        # Filter only items of type "lab"
        labs = [item for item in items if item.get("type") == "lab"]
        
        if not labs:
            return "⚠️ No labs found in the system."
        
        # Format lab list
        lab_lines = [f"- {lab['title']}" for lab in labs]
        return "📚 Available labs:\n" + "\n".join(lab_lines)
        
    except BackendError as e:
        return f"❌ Error fetching labs: {str(e)}"
