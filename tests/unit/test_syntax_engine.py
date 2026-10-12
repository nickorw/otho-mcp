import pytest
from src.engine.syntax_engine import validate_syntax


VALID_TURTLE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/onto> a owl:Ontology .
<http://example.org/onto#Person> a owl:Class ;
    rdfs:label "Person" .
"""

INVALID_TURTLE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
This is not valid turtle content @@@ !!!
"""


def test_valid_turtle_returns_ok():
    result = validate_syntax(VALID_TURTLE, format="turtle")
    assert result["valid"] is True
    assert result["error"] is None
    assert result["triple_count"] > 0


def test_invalid_turtle_returns_error():
    result = validate_syntax(INVALID_TURTLE, format="turtle")
    assert result["valid"] is False
    assert result["error"] is not None
    assert "syntax" in result["error"].lower() or "parse" in result["error"].lower()


def test_empty_content_returns_error():
    result = validate_syntax("", format="turtle")
    assert result["valid"] is False
