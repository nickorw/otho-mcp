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

    def review_owl_file(
        self,
        owl_file_path: str,
        pitfalls: Optional[List[str]] = None,
        output_format: str = "XML",
    ) -> str:
        """
        Analyzes the given OWL file and returns the OOPs! pitfall report as XML.
        """
        with open(owl_file_path, "r", encoding="utf-8") as f:
            owl_content = f.read()
        return self.review_owl_content(
            owl_content, pitfalls=pitfalls, output_format=output_format
        )

    def review_owl_content(
        self,
        owl_content: str,
        pitfalls: Optional[List[str]] = None,
        output_format: str = "XML",
    ) -> str:
        """
        Analyzes the given OWL content string and returns the OOPs! pitfall report as XML.
        Converts received OWL in turtle to RDF-XML as pre-req for Oops! API.
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

        save_text_file(f"data/output/xml_combined_owl.xml", owl_content_xml)

        with open("data/output/xml_combined_owl.xml", "r", encoding="utf-8") as f:
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
