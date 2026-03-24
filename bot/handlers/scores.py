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
        
        # Format pass rates - API returns list of dicts with task, avg_score, attempts
        lines = [f"📈 Pass rates for {lab_name}:"]
        for task_data in pass_rates:
            task_name = task_data.get("task", "Unknown task")
            avg_score = task_data.get("avg_score", 0)
            attempts = task_data.get("attempts", 0)
            lines.append(f"- {task_name}: {avg_score:.1f}% ({int(attempts)} attempts)")
        
        return "\n".join(lines)
        
    except BackendError as e:
        return f"❌ Error fetching scores: {str(e)}"
