"""
Comprehensive logging for agent execution.

Provides detailed logging of agent conversations, tool calls, and execution flow
using both file-based logging and structured JSON output.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utils.timing import format_duration


class AgentLogger:
    """
    Logger for agent execution with support for multiple output formats.

    Logs to:
    - Console (INFO level)
    - File log (DEBUG level with detailed formatting)
    - JSON structured log (complete conversation history)

    Supports iteration mode where multiple iterations append to the same log files
    with clear separation markers between iterations.
    """

    def __init__(
        self,
        story_id: str,
        log_dir: str = "logs",
        agent_type: str = "generator",
        timestamp: Optional[str] = None,
        iteration: int = 1,
    ):
        """
        Initialize agent logger.

        Args:
            story_id: Story identifier for log file naming
            log_dir: Directory for log files (default: logs/)
            agent_type: Type of agent ('generator' or 'reviewer') for log file naming
            timestamp: Pre-defined timestamp for log file naming (shared across iterations).
                       If None, a new timestamp is generated.
            iteration: Current iteration number (1, 2, 3...). Used for clear separation
                       in logs when appending multiple iterations.
        """
        self.story_id = story_id
        self.agent_type = agent_type
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.iteration = iteration

        # Use provided timestamp or create new one
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

        # Set up file logger with agent type in filename
        self.text_log_path = (
            self.log_dir / f"{story_id}_{agent_type}_{self.timestamp}.log"
        )
        self.json_log_path = (
            self.log_dir / f"{story_id}_{agent_type}_{self.timestamp}.json"
        )

        # Determine if we're appending to existing logs
        self.is_appending = iteration > 1 and self.json_log_path.exists()

        # Configure Python logger
        self.logger = logging.getLogger(f"agent.{story_id}.{self.timestamp}")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # File handler - append mode for iterations 2+, write mode for iteration 1
        file_mode = "a" if self.is_appending else "w"
        file_handler = logging.FileHandler(
            self.text_log_path, mode=file_mode, encoding="utf-8"
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

        # Load existing JSON data if appending, otherwise create new structure
        if self.is_appending:
            try:
                with open(self.json_log_path, "r", encoding="utf-8") as f:
                    self.json_data = json.load(f)
                # Add a new iteration entry
                if "iterations" not in self.json_data:
                    # Migrate old format to new iterations format
                    old_data = {
                        "iteration": 1,
                        "start_time": self.json_data.get("start_time"),
                        "end_time": self.json_data.get("end_time"),
                        "messages": self.json_data.get("messages", []),
                        "tool_calls": self.json_data.get("tool_calls", []),
                        "errors": self.json_data.get("errors", []),
                        "metadata": self.json_data.get("metadata", {}),
                    }
                    self.json_data["iterations"] = [old_data]
                    # Remove old top-level fields that are now in iterations
                    for key in [
                        "messages",
                        "tool_calls",
                        "errors",
                        "metadata",
                        "end_time",
                    ]:
                        self.json_data.pop(key, None)
            except (json.JSONDecodeError, FileNotFoundError):
                self.is_appending = False
                self._init_new_json_structure()
        else:
            self._init_new_json_structure()

        # Log iteration separator for appending mode
        if self.is_appending:
            self.logger.info(f"\n{'#' * 80}")
            self.logger.info(f"{'#' * 80}")
            self.logger.info(
                f"##  ITERATION {iteration} - {datetime.now().isoformat()}"
            )
            self.logger.info(f"{'#' * 80}")
            self.logger.info(f"{'#' * 80}\n")
        else:
            self.logger.info(f"{'=' * 60}")
            self.logger.info(f"Agent Logger Initialized for {story_id}")
            self.logger.info(f"Log files: {self.text_log_path.name}")
            self.logger.info(f"Timestamp: {self.timestamp}")
            self.logger.info(f"{'=' * 60}")
            if iteration > 1:
                self.logger.info(f"\n{'#' * 80}")
                self.logger.info(f"##  ITERATION {iteration}")
                self.logger.info(f"{'#' * 80}\n")

    def _init_new_json_structure(self):
        """Initialize a new JSON data structure with iterations support."""
        self.json_data = {
            "story_id": self.story_id,
            "agent_type": self.agent_type,
            "timestamp": self.timestamp,
            "run_start_time": datetime.now().isoformat(),
            "iterations": [],
        }
        # Initialize current iteration data
        self._current_iteration_data = {
            "iteration": self.iteration,
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "tool_calls": [],
            "errors": [],
            "metadata": {},
        }

    @property
    def _current_iteration(self) -> Dict[str, Any]:
        """Get or create the current iteration data structure."""
        if hasattr(self, "_current_iteration_data"):
            return self._current_iteration_data

        # Find or create iteration entry
        for iter_data in self.json_data.get("iterations", []):
            if iter_data.get("iteration") == self.iteration:
                self._current_iteration_data = iter_data
                return self._current_iteration_data

        # Create new iteration entry
        self._current_iteration_data = {
            "iteration": self.iteration,
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "tool_calls": [],
            "errors": [],
            "metadata": {},
        }
        return self._current_iteration_data

    def log_agent_start(
        self, prompt_length: int, num_tools: int, tool_names: List[str]
    ) -> float:
        """
        Log agent initialization details.

        Args:
            prompt_length: Length of the prompt in characters
            num_tools: Number of tools available to the agent
            tool_names: List of tool names

        Returns:
            Start time as float (time.time()) for duration calculations
        """
        # Record start time for duration calculation
        self._agent_start_time = time.time()

        self.logger.info(f"Starting React agent execution (Iteration {self.iteration})")
        self.logger.debug(f"Prompt length: {prompt_length} characters")
        self.logger.debug(f"Tools available: {num_tools}")
        for tool_name in tool_names:
            self.logger.debug(f"  - {tool_name}")

        # Store in current iteration
        self._current_iteration["metadata"]["prompt_length"] = prompt_length
        self._current_iteration["metadata"]["num_tools"] = num_tools
        self._current_iteration["metadata"]["tool_names"] = tool_names
        self._current_iteration["metadata"]["agent_start_time"] = (
            datetime.now().isoformat()
        )

        return self._agent_start_time

    def log_llm_model(self, model_name: str):
        """Log the LLM model being used."""
        self.logger.info(f"LLM Model: {model_name}")
        self._current_iteration["metadata"]["llm_model"] = model_name

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

        # For ToolMessage, log which tool returned the content
        if msg_type == "ToolMessage":
            tool_name = getattr(message, "name", None)
            if tool_name:
                self.logger.debug(f"Tool: {tool_name}")

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

                # Add to current iteration's tool call log
                self._current_iteration["tool_calls"].append(
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

        # For ToolMessage, also capture the tool name that returned the content
        tool_name_for_msg = None
        if msg_type == "ToolMessage":
            tool_name_for_msg = getattr(message, "name", None)

        # Store in current iteration's JSON structure
        msg_data = {
            "index": index,
            "type": msg_type,
            "tool_name": tool_name_for_msg,  # Only populated for ToolMessage
            "content": str(content) if content else None,
            "tool_calls": tool_calls,
            "additional_kwargs": additional_kwargs,
        }
        self._current_iteration["messages"].append(msg_data)

    def log_agent_complete(self, message_count: int, workspace_state: Dict[str, Any]):
        """
        Log agent completion.

        Args:
            message_count: Total messages in conversation
            workspace_state: Final workspace state
        """
        # Calculate duration
        duration_seconds = 0.0
        if hasattr(self, "_agent_start_time"):
            duration_seconds = time.time() - self._agent_start_time

        tool_call_count = len(self._current_iteration["tool_calls"])

        self.logger.info(f"\n{'=' * 60}")
        self.logger.info(f"Agent Execution Complete (Iteration {self.iteration})")
        self.logger.info(f"{'=' * 60}")
        self.logger.info(f"Total messages: {message_count}")
        self.logger.info(f"Tool calls made: {tool_call_count}")
        self.logger.info(
            f"Generator duration: {duration_seconds:.2f}s ({format_duration(duration_seconds)})"
        )

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

        # Store in current iteration
        self._current_iteration["metadata"]["message_count"] = message_count
        self._current_iteration["metadata"]["tool_call_count"] = tool_call_count
        self._current_iteration["metadata"]["duration_seconds"] = round(
            duration_seconds, 2
        )
        self._current_iteration["metadata"]["duration_formatted"] = format_duration(
            duration_seconds
        )
        self._current_iteration["workspace_state"] = workspace_state
        self._current_iteration["end_time"] = datetime.now().isoformat()

    def log_error(self, error: Exception):
        """Log an error that occurred during execution."""
        self.logger.error(f"ERROR: {str(error)}")
        import traceback

        tb = traceback.format_exc()
        self.logger.debug(f"Traceback:\n{tb}")

        # Store in current iteration
        self._current_iteration["errors"].append(
            {
                "error": str(error),
                "traceback": tb,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def save_json_log(self):
        """Save structured JSON log to file, adding current iteration to iterations list."""
        try:
            # Add current iteration data to iterations list if not already there
            iteration_exists = any(
                iter_data.get("iteration") == self.iteration
                for iter_data in self.json_data.get("iterations", [])
            )
            if not iteration_exists:
                self.json_data["iterations"].append(self._current_iteration)

            # Update run end time
            self.json_data["run_end_time"] = datetime.now().isoformat()

            with open(self.json_log_path, "w", encoding="utf-8") as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"JSON log saved: {self.json_log_path}")
        except Exception as e:
            self.logger.error(f"Failed to save JSON log: {e}")

    def get_log_paths(self) -> Dict[str, Path]:
        """Get paths to log files."""
        return {"text_log": self.text_log_path, "json_log": self.json_log_path}

    def get_duration_seconds(self) -> float:
        """Get the duration of the current agent execution in seconds."""
        return self._current_iteration.get("metadata", {}).get("duration_seconds", 0.0)
