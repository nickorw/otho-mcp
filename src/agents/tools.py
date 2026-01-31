"""
Standalone validation tools for the React agent.

These tools provide syntax validation and pitfall checking capabilities
for the agent to self-validate its generated ontologies.
"""

import os
import tempfile
import uuid
from datetime import datetime
from typing import Any, Dict

from langchain.tools import tool

from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.utils.oops_parser import parse_oops_response


@tool
def validate_syntax_tool(owl_content: str) -> Dict[str, Any]:
    """
    Validate RDF/Turtle syntax of OWL ontology.

    Use this tool to check if your generated OWL code has valid Turtle syntax.
    The tool uses rdflib to parse and validate the syntax.

    Args:
        owl_content: OWL ontology code in Turtle syntax

    Returns:
        Dictionary with validation results:
        - valid (bool): True if syntax is correct, False otherwise
        - error (str or None): Error message if validation failed, None if passed

    Example:
        result = validate_syntax_tool(my_owl_code)
        if result["valid"]:
            print("Syntax is correct!")
        else:
            print(f"Syntax error: {result['error']}")
    """
    try:
        reviewer = RDFSyntaxReviewer()
        result = reviewer.review_owl_content(owl_content)

        is_valid = result == "OK"
        error_msg = None if is_valid else result

        return {"valid": is_valid, "error": error_msg}
    except Exception as e:
        return {
            "valid": False,
            "error": f"Exception during syntax validation: {str(e)}",
        }


@tool
def check_pitfalls_tool(owl_content: str) -> Dict[str, Any]:
    """
    Check for OOPS ontology modeling pitfalls.

    Use this tool to validate your ontology against common modeling pitfalls
    using the OOPS (OntOlogy Pitfall Scanner) web service. The tool checks
    for 22 different types of pitfalls including missing annotations, unconnected
    classes, and other modeling issues.

    Args:
        owl_content: OWL ontology code in Turtle syntax

    Returns:
        Dictionary with pitfall analysis:
        - has_pitfalls (bool): True if pitfalls were detected
        - pitfall_count (int): Number of pitfalls found
        - pitfalls (list): List of pitfall details, each containing:
            - code (str): Pitfall code (e.g., "P04", "P08")
            - name (str): Pitfall name
            - description (str): Description of the issue
            - affected_elements (list): List of ontology elements with this pitfall

    Example:
        result = check_pitfalls_tool(my_owl_code)
        if result["has_pitfalls"]:
            print(f"Found {result['pitfall_count']} pitfalls:")
            for p in result["pitfalls"]:
                print(f"  - {p['code']}: {p['name']}")
        else:
            print("No pitfalls detected!")
    """
    # Save to temporary file for OOPS validation
    with tempfile.NamedTemporaryFile(mode="w", suffix=".owl", delete=False) as f:
        f.write(owl_content)
        temp_path = f.name

    try:
        reviewer = OopsPitfallReviewer()

        # Check for common pitfalls
        pitfalls_to_check = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "10",
            "11",
            "12",
            "13",
            "19",
            "20",
            "21",
            "22",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
        ]

        # Generate unique identifiers to prevent race conditions when multiple
        # Otho instances run concurrently. Use "tool" prefix + UUID to distinguish
        # from final validation files.
        unique_id = f"tool_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = reviewer.review_owl_file(
            temp_path,
            pitfalls=pitfalls_to_check,
            output_format="XML",
            story_id=unique_id,
            timestamp=timestamp,
        )

        pitfall_data = parse_oops_response(result)

        return {
            "has_pitfalls": pitfall_data.get("has_pitfalls", False),
            "pitfall_count": pitfall_data.get("pitfall_count", 0),
            "pitfalls": pitfall_data.get("pitfalls", []),
        }
    except Exception as e:
        return {
            "has_pitfalls": True,
            "pitfall_count": 1,
            "pitfalls": [
                {
                    "code": "ERROR",
                    "name": "Validation Exception",
                    "description": str(e),
                    "affected_elements": [],
                }
            ],
        }
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
