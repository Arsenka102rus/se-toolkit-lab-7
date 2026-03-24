"""LLM API client for intent routing."""

import httpx
from config import settings


class LLMClient:
    """Client for the LLM API with tool calling support."""

    def __init__(self):
        self.base_url = settings.llm_api_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_api_model
        self.timeout = 30.0  # seconds

    def chat_with_tools(
        self,
        messages: list[dict],
        tools: list[dict],
        max_iterations: int = 5
    ) -> str:
        """Chat with the LLM, executing tool calls as needed.
        
        Args:
            messages: Conversation history with user message
            tools: List of tool schemas the LLM can call
            max_iterations: Maximum tool call iterations
            
        Returns:
            Final response text from the LLM
        """
        import json
        
        conversation = list(messages)
        
        for iteration in range(max_iterations):
            response = self._call_llm(conversation, tools)
            
            # Check if LLM wants to call tools
            tool_calls = response.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
            
            if not tool_calls:
                # No tool calls - return the LLM's response
                return response.get("choices", [{}])[0].get("message", {}).get("content", "I couldn't process that request.")
            
            # Execute tool calls and collect results
            tool_results = []
            for tool_call in tool_calls:
                func = tool_call.get("function", {})
                tool_name = func.get("name", "")
                tool_args_str = func.get("arguments", "{}")
                
                try:
                    tool_args = json.loads(tool_args_str) if tool_args_str else {}
                except json.JSONDecodeError:
                    tool_args = {}
                
                # Execute the tool
                result = self._execute_tool(tool_name, tool_args)
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": json.dumps(result) if not isinstance(result, str) else result
                })
            
            # Add assistant's message and tool results to conversation
            conversation.append({
                "role": "assistant",
                "tool_calls": tool_calls
            })
            conversation.extend(tool_results)
        
        # Final call to get summary after all tool executions
        final_response = self._call_llm(conversation, [])
        return final_response.get("choices", [{}])[0].get("message", {}).get("content", "I processed your request but couldn't generate a response.")

    def _call_llm(self, messages: list[dict], tools: list[dict]) -> dict:
        """Make a single LLM API call."""
        import json
        
        # Build URL: base_url should be like http://localhost:42005/v1
        if self.base_url.endswith("/v1"):
            url = f"{self.base_url}/chat/completions"
        else:
            url = f"{self.base_url}/v1/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            return response.json()

    def _execute_tool(self, tool_name: str, args: dict) -> dict | list | str:
        """Execute a tool by calling the appropriate LMS API endpoint."""
        from services.lms_client import lms_client
        
        if tool_name == "get_items":
            return lms_client.get_items() or []
        elif tool_name == "get_learners":
            return lms_client.get_learners() or []
        elif tool_name == "get_scores":
            return lms_client.get_scores(args.get("lab", "")) or []
        elif tool_name == "get_pass_rates":
            return lms_client.get_pass_rates(args.get("lab", "")) or []
        elif tool_name == "get_timeline":
            return lms_client.get_timeline(args.get("lab", "")) or []
        elif tool_name == "get_groups":
            return lms_client.get_groups(args.get("lab", "")) or []
        elif tool_name == "get_top_learners":
            return lms_client.get_top_learners(args.get("lab", ""), args.get("limit", 5)) or []
        elif tool_name == "get_completion_rate":
            return lms_client.get_completion_rate(args.get("lab", "")) or {}
        elif tool_name == "trigger_sync":
            return lms_client.trigger_sync() or {}
        else:
            return {"error": f"Unknown tool: {tool_name}"}


# Global client instance
llm_client = LLMClient()
