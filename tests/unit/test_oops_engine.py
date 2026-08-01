import pytest
from unittest.mock import patch, MagicMock
from src.engine.oops_engine import run_oops_scan, parse_oops_response

SAMPLE_OOPS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:oops="http://www.oeg-upm.net/oops#">
  <rdf:Description rdf:about="http://www.oeg-upm.net/oops#pitfall">
    <oops:hasCode>P08</oops:hasCode>
    <oops:hasName>Missing annotations</oops:hasName>
    <oops:hasDescription>Missing rdfs:label or rdfs:comment</oops:hasDescription>
    <oops:hasImportanceLevel>Minor</oops:hasImportanceLevel>
    <oops:hasNumberAffectedElements>5</oops:hasNumberAffectedElements>
  </rdf:Description>
</rdf:RDF>"""


def test_parse_oops_response_extracts_pitfalls():
    result = parse_oops_response(SAMPLE_OOPS_XML)
    assert result["has_pitfalls"] is True
    assert result["pitfall_count"] >= 1
    assert any(p["code"] == "P08" for p in result["pitfalls"])


def test_parse_empty_response_no_pitfalls():
    empty_xml = '<?xml version="1.0"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:RDF>'
    result = parse_oops_response(empty_xml)
    assert result["has_pitfalls"] is False
    assert result["pitfall_count"] == 0


@patch("src.engine.oops_engine.requests.post")
def test_run_oops_scan_calls_endpoint(mock_post):
    mock_response = MagicMock()
    mock_response.text = SAMPLE_OOPS_XML
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    result = run_oops_scan("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n<http://ex.org/o> a owl:Ontology .")
    assert result["has_pitfalls"] is True
    mock_post.assert_called_once()
