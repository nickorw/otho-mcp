"""
Comprehensive logging for agent execution.

Provides detailed logging of agent conversations, tool calls, and execution flow
using both file-based logging and structured JSON output.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AgentLogger:
    """
    Logger for agent execution with support for multiple output formats.

    Logs to:
    - Console (INFO level)
    - File log (DEBUG level with detailed formatting)
    - JSON structured log (complete conversation history)
    """

    def __init__(self, story_id: str, log_dir: str = "logs"):
        """
        Initialize agent logger.

        Args:
            story_id: Story identifier for log file naming
            log_dir: Directory for log files (default: logs/)
        """
        self.story_id = story_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create timestamp for this run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Set up file logger
        self.text_log_path = self.log_dir / f"{story_id}_agent_{self.timestamp}.log"
        self.json_log_path = self.log_dir / f"{story_id}_agent_{self.timestamp}.json"

        # Configure Python logger
        self.logger = logging.getLogger(f"agent.{story_id}")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # File handler - detailed DEBUG logs
        file_handler = logging.FileHandler(
            self.text_log_path, mode="w", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler - INFO and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Structured data for JSON log
        self.json_data = {
            "story_id": story_id,
            "timestamp": self.timestamp,
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "tool_calls": [],
            "errors": [],
            "metadata": {},
        }

        self.logger.info(f"{'=' * 60}")
        self.logger.info(f"Agent Logger Initialized for {story_id}")
        self.logger.info(f"Log files: {self.text_log_path.name}")
        self.logger.info(f"{'=' * 60}")

    def log_agent_start(
        self, prompt_length: int, num_tools: int, tool_names: List[str]
    ):
        """Log agent initialization details."""
        self.logger.info("Starting React agent execution")
        self.logger.debug(f"Prompt length: {prompt_length} characters")
        self.logger.debug(f"Tools available: {num_tools}")
        for tool_name in tool_names:
            self.logger.debug(f"  - {tool_name}")

        self.json_data["metadata"]["prompt_length"] = prompt_length
        self.json_data["metadata"]["num_tools"] = num_tools
        self.json_data["metadata"]["tool_names"] = tool_names

    def log_message(self, index: int, message: Any):
        """
        Log a single message from the agent conversation.

        Args:
            index: Message index in conversation
            message: Message object (HumanMessage, AIMessage, ToolMessage, etc.)
        """
        msg_type = type(message).__name__
        self.logger.debug(f"\n{'=' * 60}")
        self.logger.debug(f"Message {index}: {msg_type}")
        self.logger.debug(f"{'=' * 60}")

        # Extract content
        content = None
        if hasattr(message, "content"):
            content = message.content
            if content:
                # Log full content to file, truncated to console
                self.logger.debug(f"Content ({len(str(content))} chars):")
                content_str = str(content)
                if len(content_str) > 1000:
                    self.logger.debug(
                        content_str[:1000]
                        + f"\n... ({len(content_str) - 1000} more chars)"
                    )
                else:
                    self.logger.debug(content_str)

        # Extract tool calls
        tool_calls = []
        if hasattr(message, "tool_calls") and message.tool_calls:
            self.logger.debug(f"\nTool Calls: {len(message.tool_calls)}")
            for i, tc in enumerate(message.tool_calls):
                if isinstance(tc, dict):
                    tool_name = tc.get("name", "unknown")
                    tool_args = tc.get("args", {})
                    tool_id = tc.get("id", f"call_{i}")
                else:
                    tool_name = getattr(tc, "name", "unknown")
                    tool_args = getattr(tc, "args", {})
                    tool_id = getattr(tc, "id", f"call_{i}")

                self.logger.debug(f"  Tool {i + 1}: {tool_name}")
                self.logger.debug(f"    ID: {tool_id}")
                self.logger.debug(f"    Args: {json.dumps(tool_args, indent=6)}")

                tool_calls.append(
                    {"index": i, "name": tool_name, "id": tool_id, "args": tool_args}
                )

                # Add to global tool call log
                self.json_data["tool_calls"].append(
                    {
                        "message_index": index,
                        "tool_index": i,
                        "name": tool_name,
                        "id": tool_id,
                        "args": tool_args,
                    }
                )

        # Extract additional info
        additional_kwargs = {}
        if hasattr(message, "additional_kwargs"):
            additional_kwargs = message.additional_kwargs
            if additional_kwargs:
                self.logger.debug(
                    f"\nAdditional kwargs: {json.dumps(additional_kwargs, indent=2)}"
                )

        # Store in JSON structure
        msg_data = {
            "index": index,
            "type": msg_type,
            "content": str(content) if content else None,
            "tool_calls": tool_calls,
            "additional_kwargs": additional_kwargs,
        }
        self.json_data["messages"].append(msg_data)

    def log_agent_complete(self, message_count: int, workspace_state: Dict[str, Any]):
        """
        Log agent completion.

        Args:
            message_count: Total messages in conversation
            workspace_state: Final workspace state
        """
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("Agent Execution Complete")
        self.logger.info(f"{'=' * 60}")
        self.logger.info(f"Total messages: {message_count}")
        self.logger.info(f"Tool calls made: {len(self.json_data['tool_calls'])}")

        # Log workspace summary
        self.logger.debug("\nFinal Workspace State:")
        self.logger.debug(
            f"  Scratchpad keys: {list(workspace_state.get('scratchpad', {}).keys())}"
        )
        self.logger.debug(
            f"  Generated OWL length: {len(workspace_state.get('generated_owl', ''))} chars"
        )
        self.logger.debug(
            f"  Iteration count: {workspace_state.get('iteration_count', 0)}"
        )

        self.json_data["metadata"]["message_count"] = message_count
        self.json_data["metadata"]["tool_call_count"] = len(
            self.json_data["tool_calls"]
        )
        self.json_data["workspace_final_state"] = workspace_state
        self.json_data["end_time"] = datetime.now().isoformat()

    def log_error(self, error: Exception):
        """Log an error that occurred during execution."""
        self.logger.error(f"ERROR: {str(error)}")
        import traceback

        tb = traceback.format_exc()
        self.logger.debug(f"Traceback:\n{tb}")

        self.json_data["errors"].append(
            {
                "error": str(error),
                "traceback": tb,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def save_json_log(self):
        """Save structured JSON log to file."""
        try:
            with open(self.json_log_path, "w", encoding="utf-8") as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"JSON log saved: {self.json_log_path}")
        except Exception as e:
            self.logger.error(f"Failed to save JSON log: {e}")

    def get_log_paths(self) -> Dict[str, Path]:
        """Get paths to log files."""
        return {"text_log": self.text_log_path, "json_log": self.json_log_path}
