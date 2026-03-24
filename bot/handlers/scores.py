"""Handler for /scores command."""


def handle_scores(lab_name: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        lab_name: Optional lab identifier (e.g., "lab-01")
    
    Returns:
        Pass rates for tasks (placeholder for now).
    """
    # TODO: Task 2 - Call backend /analytics endpoint
    if lab_name:
        return f"📊 Scores for {lab_name}: (not yet implemented)"
    return "📊 Scores: Please specify a lab (e.g., /scores lab-01)"
