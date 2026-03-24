"""Intent router that uses LLM to decide which tools to call."""

import sys
from services.llm_client import llm_client

# System prompt that teaches the LLM how to use tools
SYSTEM_PROMPT = """You are a helpful assistant for a Learning Management System (LMS). 
You have access to tools that fetch data from the LMS backend. 

When a user asks a question, you should:
1. Analyze what information they need
2. Call the appropriate tools to fetch that data
3. Use the tool results to provide a helpful, accurate answer

If the user asks about labs, scores, students, or analytics - use your tools to get real data.
If the user greets you or asks something unrelated, respond naturally without using tools.

Always base your answers on the actual data returned by tools, not assumptions."""

# Tool definitions - 9 backend endpoints as LLM tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks. Use this to find available labs or when user asks what's available.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of all enrolled learners/students. Use when user asks about enrollment, how many students, or learner details.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab. Use when user asks about score distribution or how students performed overall.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a lab. Use when user asks about task difficulty, pass rates, or scores for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day for a lab. Use when user asks about submission timeline, activity over time, or when students submitted.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a lab. Use when user asks about group comparison, which group is best, or group performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by average score for a lab. Use when user asks about top students, leaderboard, or best performers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"},
                    "limit": {"type": "integer", "description": "Number of top learners to return (default: 5)"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate (percentage of learners with score >= 60) for a lab. Use when user asks about completion rate or how many students passed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01', 'lab-04'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger data sync from autochecker API. Use when user asks to refresh data, update scores, or sync the system.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


def route_intent(message: str) -> str:
    """Route a user message through the LLM intent router.
    
    Args:
        message: User's natural language message
        
    Returns:
        Response text from the LLM
    """
    # Build conversation with system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]
    
    # Debug output to stderr (visible in --test mode)
    print(f"[intent] Processing: {message}", file=sys.stderr)
    
    try:
        response = llm_client.chat_with_tools(messages, TOOLS)
        print(f"[response] {response[:100]}...", file=sys.stderr)
        return response
    except Exception as e:
        error_msg = str(e)
        print(f"[error] LLM error: {error_msg}", file=sys.stderr)
        
        # Handle common errors
        if "401" in error_msg or "Unauthorized" in error_msg:
            return "LLM authentication error (HTTP 401). The Qwen OAuth token may have expired. Try: cd ~/qwen-code-oai-proxy && docker compose restart"
        elif "connection refused" in error_msg or "502" in error_msg:
            return f"LLM service unavailable: {error_msg}. Check that the LLM proxy is running."
        else:
            return f"LLM error: {error_msg}"
