"""AI Budget Agent using Claude with tool use."""

import json
from typing import Optional
from anthropic import Anthropic
from src.config import ANTHROPIC_API_KEY
from src.tools import TOOLS, process_tool


class BudgetAgent:
    """Agent for managing budget with Claude API and tool use."""

    def __init__(self):
        """Initialize the budget agent."""
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []

        self.system_prompt = """You are a helpful personal budget assistant. You help users manage their finances by:
- Recording expenses and income sources
- Tracking partial payments
- Managing budget-related tasks
- Providing budget summaries and insights

Always be friendly, helpful, and encourage good financial habits. When users ask about their budget, analyze the data
and provide actionable insights. Use the available tools to help manage their finances.

Today's date is 2026-04-02. When suggesting dates, use this as reference."""

    def chat(self, user_message: str) -> str:
        """Send a message and get a response with tool use support."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self.system_prompt,
                tools=TOOLS,
                messages=self.conversation_history
            )

            # Process response
            assistant_message = {"role": "assistant", "content": response.content}
            self.conversation_history.append(assistant_message)

            # Check if we need to process tools
            if response.stop_reason == "tool_use":
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_use_id = block.id

                        # Process the tool
                        tool_result = process_tool(tool_name, tool_input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": tool_result
                        })

                # Add tool results to conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

            else:
                # Extract final text response
                final_response = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_response += block.text

                return final_response

        return "Max iterations reached. Please try again."

    def reset(self):
        """Reset conversation history."""
        self.conversation_history = []
