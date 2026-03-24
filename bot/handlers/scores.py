"""Handler for /scores command."""

from services.lms_client import lms_client, BackendError


def handle_scores(lab_name: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        lab_name: Optional lab identifier (e.g., "lab-01")
    
    Returns:
        Pass rates for tasks in the specified lab.
    """
    if not lab_name:
        return "📊 Scores: Please specify a lab (e.g., /scores lab-01)"
    
    try:
        pass_rates = lms_client.get_pass_rates(lab_name)
        
        if pass_rates is None:
            return f"⚠️ No scores found for {lab_name}."
        
        if not pass_rates:
            return f"⚠️ Lab {lab_name} has no submission data yet."
        
        # Format pass rates - each item is a dict with task info
        lines = [f"📈 Pass rates for {lab_name}:"]
        for task_data in pass_rates:
            # Extract task name and pass rate from the response
            # The API returns a list of dicts with task info
            for task_name, rate in task_data.items():
                if isinstance(rate, (int, float)):
                    lines.append(f"- {task_name}: {rate:.1f}%")
        
        return "\n".join(lines)
        
    except BackendError as e:
        return f"❌ Error fetching scores: {str(e)}"
