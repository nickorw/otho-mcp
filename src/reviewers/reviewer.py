from typing import Any, List, Optional

import requests
from rdflib import Graph

from src.utils.file_handler import save_text_file


class OopsPitfallReviewer:
    """
    Reviewer class that uses the OOPs! Pitfall Scanner service to analyze OWL ontologies.
    """

    def __init__(self, endpoint: str = "http://localhost/OOPS/rest"):
        self.endpoint = endpoint
        self._last_rdfxml_path: Optional[str] = None  # Track last generated file path

    @property
    def last_rdfxml_path(self) -> Optional[str]:
        """Get the path of the last generated RDF/XML file for use by reasoners."""
        return self._last_rdfxml_path

    def review_owl_file(
        self,
        owl_file_path: str,
        pitfalls: Optional[List[str]] = None,
        output_format: str = "XML",
        story_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> str:
        """
        Analyzes the given OWL file and returns the OOPs! pitfall report as XML.
        """
        with open(owl_file_path, "r", encoding="utf-8") as f:
            owl_content = f.read()
        return self.review_owl_content(
            owl_content,
            pitfalls=pitfalls,
            output_format=output_format,
            story_id=story_id,
            timestamp=timestamp,
        )

    def review_owl_content(
        self,
        owl_content: str,
        pitfalls: Optional[List[str]] = None,
        output_format: str = "XML",
        story_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> str:
        """
        Analyzes the given OWL content string and returns the OOPs! pitfall report as XML.
        Converts received OWL in turtle to RDF-XML as pre-req for Oops! API.

        Args:
            owl_content: OWL ontology content in Turtle format
            pitfalls: List of pitfall IDs to check for
            output_format: Output format (default: XML)
            story_id: Story identifier for unique file naming (prevents race conditions)
            timestamp: Timestamp for unique file naming (prevents race conditions)
        """

        # Convert Turtle to RDF/XML to use in Oops!
        try:
            g = Graph()
            g.parse(data=owl_content, format="turtle")

            owl_content_xml_brute = g.serialize(format="xml")
            owl_content_xml = owl_content_xml_brute.replace("'", "").replace("\n", "")

            # Print the first 5 lines of the serialized RDF/XML
            # owl_lines = owl_content_xml.splitlines()
            # print("First 5 lines of owl_content_xml:")
            # for line in owl_lines[:5]:
            #     print(line)
        except Exception as e:
            raise ValueError(f"Failed to convert Turtle to RDF/XML: {e}")

        # Generate unique filename to prevent race conditions when running multiple instances
        # story_id and timestamp are REQUIRED to prevent race conditions
        if not story_id or not timestamp:
            raise ValueError(
                "story_id and timestamp are required for unique xml_combined_owl file naming. "
                f"Received: story_id={story_id!r}, timestamp={timestamp!r}"
            )
        rdfxml_filename = f"xml_combined_owl_{story_id}_{timestamp}.xml"

        rdfxml_path = f"data/output/{rdfxml_filename}"
        self._last_rdfxml_path = rdfxml_path  # Store for reasoners to use

        save_text_file(rdfxml_path, owl_content_xml)

        with open(rdfxml_path, "r", encoding="utf-8") as f:
            owl_content_xml_final = f.read()
        print("Running Oops API...")
        pitfalls_str = ""
        if pitfalls:
            pitfalls_str = ",".join(pitfalls)
        xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <OOPSRequest>
                    <OntologyURI>http://www.example.org/testontology</OntologyURI>
                    <OntologyContent><![CDATA[{owl_content_xml_final}]]></OntologyContent>
                    <Pitfalls>{pitfalls_str}</Pitfalls>
                    <OutputFormat>{output_format}</OutputFormat>
                    </OOPSRequest>"""
        headers = {"Content-Type": "application/xml"}
        response = requests.post(
            self.endpoint, data=xml_body.encode("utf-8"), headers=headers
        )
        response.raise_for_status()
        return response.text


class RDFSyntaxReviewer:
    """
    Reviewer class that uses rdflib to validate RDF/OWL/RDFS syntax.
    """

    def __init__(self, format: str = "turtle"):
        self.format = format  # e.g., 'xml', 'turtle', 'n3', etc.

    def review_owl_content(self, owl_content: str) -> str:
        """
        Validate the given OWL/RDF content string for syntax errors.
        Returns 'OK' if valid, else raises an exception with the error message.
        """
        g = Graph()
        try:
            g.parse(data=owl_content, format=self.format)
            return "OK"
        except Exception as e:
            raise ValueError(f"RDF syntax error: {e}")
