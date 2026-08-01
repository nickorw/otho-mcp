import xml.etree.ElementTree as ET
from typing import Optional

import requests
from rdflib import Graph

from src.core.config import settings

ALL_PITFALLS = "2,3,4,5,6,7,8,10,11,12,13,19,20,21,22,24,25,26,27,28,29"

IMPORTANCE_ORDER = {"Critical": 0, "Important": 1, "Minor": 2}


def _content_to_rdfxml(content: str, input_format: str = "turtle") -> str:
    """Convert ontology content to RDF/XML string for OOPs API."""
    g = Graph()
    g.parse(data=content, format=input_format)
    xml_str = g.serialize(format="xml")
    return xml_str.replace("'", "").replace("\n", "")


def run_oops_scan(
    content: str,
    pitfalls: Optional[str] = None,
    oops_url: Optional[str] = None,
    input_format: str = "turtle",
) -> dict:
    """Send ontology content to OOPs service and return parsed results."""
    url = oops_url or settings.oops_url
    pitfalls_str = pitfalls or ALL_PITFALLS

    try:
        rdfxml_content = _content_to_rdfxml(content, input_format=input_format)
    except Exception as e:
        return {
            "has_pitfalls": False,
            "pitfall_count": 0,
            "pitfalls": [],
            "error": f"Failed to convert to RDF/XML: {e}",
        }

    xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<OOPSRequest>
<OntologyURI>http://www.example.org/ontology</OntologyURI>
<OntologyContent><![CDATA[{rdfxml_content}]]></OntologyContent>
<Pitfalls>{pitfalls_str}</Pitfalls>
<OutputFormat>XML</OutputFormat>
</OOPSRequest>"""

    headers = {"Content-Type": "application/xml"}
    response = requests.post(url, data=xml_body.encode("utf-8"), headers=headers)
    response.raise_for_status()
    return parse_oops_response(response.text)


def parse_oops_response(xml_text: str) -> dict:
    """Parse OOPs XML response into structured dict."""
    pitfalls = []
    try:
        root = ET.fromstring(xml_text)
        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "oops": "http://www.oeg-upm.net/oops#",
        }

        for desc in root.findall(".//rdf:Description", ns):
            code_el = desc.find("oops:hasCode", ns)
            if code_el is None:
                continue
            pitfall = {
                "code": code_el.text.strip() if code_el.text else "",
                "name": _get_text(desc, "oops:hasName", ns),
                "description": _get_text(desc, "oops:hasDescription", ns),
                "importance": _get_text(desc, "oops:hasImportanceLevel", ns),
                "affected_elements": int(_get_text(desc, "oops:hasNumberAffectedElements", ns) or "0"),
            }
            pitfalls.append(pitfall)
    except ET.ParseError:
        pass

    pitfalls.sort(key=lambda p: IMPORTANCE_ORDER.get(p.get("importance", ""), 99))

    return {
        "has_pitfalls": len(pitfalls) > 0,
        "pitfall_count": len(pitfalls),
        "pitfalls": pitfalls,
    }


def _get_text(element, tag: str, ns: dict) -> str:
    el = element.find(tag, ns)
    return el.text.strip() if el is not None and el.text else ""
