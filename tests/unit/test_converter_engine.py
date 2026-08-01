import pytest
from src.engine.converter_engine import convert_format, SUPPORTED_FORMATS

TURTLE_CONTENT = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
<http://example.org/onto> a owl:Ontology .
"""


def test_turtle_to_xml_roundtrip():
    xml_result = convert_format(TURTLE_CONTENT, "turtle", "xml")
    assert "rdf:RDF" in xml_result or "RDF" in xml_result


def test_unsupported_format_raises():
    with pytest.raises(ValueError, match="Unsupported"):
        convert_format(TURTLE_CONTENT, "turtle", "banana")


def test_supported_formats_list():
    assert "turtle" in SUPPORTED_FORMATS
    assert "xml" in SUPPORTED_FORMATS
    assert "json-ld" in SUPPORTED_FORMATS
