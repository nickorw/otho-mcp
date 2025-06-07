import requests
from typing import Any, Optional, List

class OopsPitfallReviewer:
    """
    Reviewer class that uses the OOPs! Pitfall Scanner web service to analyze OWL ontologies.
    """
    def __init__(self, endpoint: str = "http://localhost/OOPS/rest" ):
        self.endpoint = endpoint

    def review_owl_file(self, owl_file_path: str, pitfalls: Optional[List[str]] = None, output_format: str = "XML") -> str:
        """
        Analyze the given OWL file and return the OOPs! pitfall report as XML.
        """
        with open(owl_file_path, 'r', encoding='utf-8') as f:
            owl_content = f.read()
        return self.review_owl_content(owl_content, pitfalls=pitfalls, output_format=output_format)

    def review_owl_content(self, owl_content: str, pitfalls: Optional[List[str]] = None, output_format: str = "XML") -> str:
        """
        Analyze the given OWL content string and return the OOPs! pitfall report as XML.
        """
        pitfalls_str = ''
        if pitfalls:
            pitfalls_str = ','.join(pitfalls)
        xml_body = f'''<?xml version="1.0" encoding="UTF-8"?>
                    <OOPSRequest>
                    <OntologyURI>http://www.example.org/testontology</OntologyURI>
                    <OntologyContent><![CDATA[{owl_content}]]></OntologyContent>
                    <Pitfalls>{pitfalls_str}</Pitfalls>
                    <OutputFormat>{output_format}</OutputFormat>
                    </OOPSRequest>'''
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.endpoint, data=xml_body.encode('utf-8'), headers=headers)
        response.raise_for_status()
        return response.text