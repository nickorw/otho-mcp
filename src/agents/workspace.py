"""
AgentWorkspace: Mutable container for agent's working memory and output.

This class provides a shared mutable workspace that tools can modify while
respecting LangGraph's immutable state pattern. The workspace is wrapped in
a List and stored in state, allowing tools to mutate the workspace object
while the state dict remains immutable.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentWorkspace:
    """
    Mutable workspace for agent's planning, progress tracking, and output.

    This class instance is shared between the node and tools, enabling
    tools to modify data while respecting LangGraph's immutable state pattern.

    Attributes:
        scratchpad: Dictionary for agent's working memory (plans, iterations, notes)
        generated_owl: Final OWL ontology content
    """

    scratchpad: Dict[str, Any] = field(default_factory=dict)
    generated_owl: str = ""

    def update_scratchpad(self, key: str, value: Any) -> bool:
        """
        Update scratchpad entry.

        Args:
            key: Scratchpad key (e.g., "plan", "iterations", "cq_coverage")
            value: Value to store (can be dict, list, string, etc.)

        Returns:
            True if update successful
        """
        self.scratchpad[key] = value
        return True

    def get_scratchpad(self, key: str) -> Any:
        """
        Read scratchpad entry.

        Args:
            key: Scratchpad key to retrieve

        Returns:
            Value stored at key, or None if not found
        """
        return self.scratchpad.get(key)

    def save_ontology(self, owl_content: str) -> bool:
        """
        Save ontology to workspace.

        Args:
            owl_content: Complete OWL ontology in Turtle syntax

        Returns:
            True if save successful
        """
        self.generated_owl = owl_content
        return True

    def get_iteration_count(self) -> int:
        """
        Count iterations from scratchpad.

        Returns:
            Number of validation iterations logged in scratchpad
        """
        iterations = self.scratchpad.get("iterations", [])
        return len(iterations) if isinstance(iterations, list) else 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Export workspace for JSON serialization.

        Returns:
            Dictionary representation of workspace state
        """
        return {
            "scratchpad": self.scratchpad,
            "generated_owl": self.generated_owl,
            "iteration_count": self.get_iteration_count(),
        }
