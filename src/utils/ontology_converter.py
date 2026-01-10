#!/usr/bin/env python3
"""
Ontology format converter - Convert between RDF formats (turtle, xml, n3, nt, json-ld)

USAGE: python src/utils/ontology_converter.py input.owl output.xml [input_fmt] [output_fmt]
EXAMPLE: python src/utils/ontology_converter.py data/output/file.owl data/output/file.xml
"""

from pathlib import Path
from typing import Optional

from rdflib import Graph


def convert_ontology_format(
    input_file: str,
    output_file: str,
    input_format: str = "turtle",
    output_format: str = "xml",
) -> bool:
    """
    Convert an ontology file from one RDF format to another.

    Args:
        input_file: Path to the input ontology file
        output_file: Path to the output ontology file
        input_format: Format of the input file (default: 'turtle')
                     Supported: 'turtle', 'xml', 'n3', 'nt', 'json-ld'
        output_format: Format of the output file (default: 'xml')
                      Supported: 'turtle', 'xml', 'n3', 'nt', 'json-ld', 'pretty-xml'

    Returns:
        bool: True if conversion was successful, False otherwise

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If format is not supported
    """
    # Validate input file exists
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    print(f"Reading {input_format.upper()} file: {input_file}")

    try:
        # Create a new graph
        g = Graph()

        # Parse the input file
        g.parse(input_file, format=input_format)

        print(f"Parsed {len(g)} triples from the input file")

        # Serialize to output format
        print(f"Writing {output_format.upper()} file: {output_file}")
        g.serialize(destination=output_file, format=output_format)

        print("Conversion completed successfully!")
        return True

    except Exception as e:
        print(f"Error during conversion: {e}")
        return False


def turtle_to_xml(input_file: str, output_file: Optional[str] = None) -> bool:
    """
    Convenience function to convert Turtle to XML/RDF.

    Args:
        input_file: Path to the input Turtle file
        output_file: Path to the output XML file (optional, defaults to .xml extension)

    Returns:
        bool: True if conversion was successful, False otherwise
    """
    if output_file is None:
        output_file = str(Path(input_file).with_suffix(".xml"))

    return convert_ontology_format(input_file, output_file, "turtle", "xml")


def xml_to_turtle(input_file: str, output_file: Optional[str] = None) -> bool:
    """
    Convenience function to convert XML/RDF to Turtle.

    Args:
        input_file: Path to the input XML file
        output_file: Path to the output Turtle file (optional, defaults to .owl/.ttl)

    Returns:
        bool: True if conversion was successful, False otherwise
    """
    if output_file is None:
        # Use .owl extension for OWL ontologies, .ttl for plain RDF
        output_file = str(Path(input_file).with_suffix(".owl"))

    return convert_ontology_format(input_file, output_file, "xml", "turtle")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python ontology_converter.py <input_file> <output_file> [input_format] [output_format]"
        )
        print("\nSupported formats: turtle, xml, n3, nt, json-ld")
        print("\nExamples:")
        print("  python ontology_converter.py input.owl output.xml")
        print("  python ontology_converter.py input.ttl output.xml turtle xml")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    input_format = sys.argv[3] if len(sys.argv) > 3 else "turtle"
    output_format = sys.argv[4] if len(sys.argv) > 4 else "xml"

    success = convert_ontology_format(
        input_file, output_file, input_format, output_format
    )
    sys.exit(0 if success else 1)
