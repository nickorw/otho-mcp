"""
OOPS XML Parser - Extracts pitfall information from OOPS validator responses
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional


def parse_oops_response(oops_xml: str) -> Dict:
    """
    Parse OOPS XML response and extract pitfall information.

    Args:
        oops_xml: XML string from OOPS validator

    Returns:
        Dictionary with pitfall summary and details
    """
    try:
        # Handle the case where XML is wrapped in text
        if "<?xml" in oops_xml:
            xml_start = oops_xml.find("<?xml")
            oops_xml = oops_xml[xml_start:]

        root = ET.fromstring(oops_xml)

        # Detect wrong_execution error response from OOPS
        if "wrong_execution" in oops_xml:
            error_msg = "OOPS could not analyse the ontology (wrong_execution response)"
            print(f"OOPS wrong_execution response detected")
            return {
                "has_pitfalls": True,
                "pitfall_count": 0,
                "pitfalls": [],
                "oops_error": True,
                "error": error_msg,
            }

        # Define namespace
        ns = {"oops": "http://www.oeg-upm.net/oops"}

        pitfalls = []
        for pitfall_elem in root.findall(".//oops:Pitfall", ns):
            code_elem = pitfall_elem.find("oops:Code", ns)
            name_elem = pitfall_elem.find("oops:Name", ns)
            desc_elem = pitfall_elem.find("oops:Description", ns)
            importance_elem = pitfall_elem.find("oops:Importance", ns)
            num_affected_elem = pitfall_elem.find("oops:NumberAffectedElements", ns)

            # Extract affected elements
            affected_elements = []
            affects_elem = pitfall_elem.find("oops:Affects", ns)
            if affects_elem is not None:
                for affected in affects_elem.findall("oops:AffectedElement", ns):
                    if affected.text:
                        affected_elements.append(affected.text.strip())

                # Also check NoInverseSuggestion container
                no_inverse = affects_elem.find("oops:NoInverseSuggestion", ns)
                if no_inverse is not None:
                    for affected in no_inverse.findall("oops:AffectedElement", ns):
                        if affected.text:
                            affected_elements.append(affected.text.strip())

            pitfall = {
                "code": code_elem.text if code_elem is not None else "Unknown",
                "name": name_elem.text if name_elem is not None else "Unknown",
                "description": desc_elem.text if desc_elem is not None else "",
                "importance": (
                    importance_elem.text if importance_elem is not None else "Unknown"
                ),
                "num_affected": (
                    int(num_affected_elem.text)
                    if num_affected_elem is not None and num_affected_elem.text
                    else len(affected_elements)
                ),
                "affected_elements": affected_elements,
            }
            pitfalls.append(pitfall)

        return {
            "has_pitfalls": len(pitfalls) > 0,
            "pitfall_count": len(pitfalls),
            "pitfalls": pitfalls,
        }

    except ET.ParseError as e:
        print(f"Error parsing OOPS XML: {e}")
        return {
            "has_pitfalls": True,
            "pitfall_count": 0,
            "pitfalls": [],
            "oops_error": True,
            "error": str(e),
        }
    except Exception as e:
        print(f"Unexpected error parsing OOPS response: {e}")
        return {
            "has_pitfalls": True,
            "pitfall_count": 0,
            "pitfalls": [],
            "oops_error": True,
            "error": str(e),
        }


def format_pitfalls_for_feedback(pitfall_data: Dict) -> str:
    """
    Format pitfall data into human-readable feedback for LLM.

    Args:
        pitfall_data: Dictionary from parse_oops_response

    Returns:
        Formatted string describing the pitfalls
    """
    if pitfall_data.get("oops_error", False):
        error_msg = pitfall_data.get("error", "Unknown error")
        return f"OOPS validation failed with error: {error_msg}\nPlease ensure the ontology doesn't have any critical mistakes and is valid."

    if not pitfall_data.get("has_pitfalls", False):
        return "No pitfalls detected."

    feedback_lines = [f"Validation found {pitfall_data['pitfall_count']} pitfall(s):\n"]

    for pitfall in pitfall_data["pitfalls"]:
        feedback_lines.append(
            f"- {pitfall['code']} ({pitfall['importance']}): {pitfall['name']}"
        )
        feedback_lines.append(f"  Description: {pitfall['description']}")
        feedback_lines.append(f"  Affected elements: {pitfall['num_affected']}")

        # Include some example affected elements (limit to 5 for readability)
        if pitfall["affected_elements"]:
            examples = pitfall["affected_elements"][:5]
            feedback_lines.append(f"  Examples: {', '.join(examples)}")
            if len(pitfall["affected_elements"]) > 5:
                remaining = len(pitfall["affected_elements"]) - 5
                feedback_lines.append(f"  ... and {remaining} more")
        feedback_lines.append("")

    return "\n".join(feedback_lines)
