import pytest
from unittest.mock import patch, MagicMock
from src.engine.oops_engine import run_oops_scan, parse_oops_response

SAMPLE_OOPS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<oops:OOPSResponse xmlns:oops="http://www.oeg-upm.net/oops">
  <oops:Pitfall>
    <oops:Code>P08</oops:Code>
    <oops:Name>Missing annotations</oops:Name>
    <oops:Description>Missing rdfs:label or rdfs:comment</oops:Description>
    <oops:Importance>Minor</oops:Importance>
    <oops:NumberAffectedElements>2</oops:NumberAffectedElements>
    <oops:Affects>
      <oops:AffectedElement>http://ex.org/o#Person</oops:AffectedElement>
      <oops:AffectedElement>http://ex.org/o#Orphan</oops:AffectedElement>
    </oops:Affects>
  </oops:Pitfall>
</oops:OOPSResponse>"""


def test_parse_oops_response_extracts_pitfalls():
    result = parse_oops_response(SAMPLE_OOPS_XML)
    assert result["has_pitfalls"] is True
    assert result["pitfall_count"] >= 1
    p = next(p for p in result["pitfalls"] if p["code"] == "P08")
    assert p["name"] == "Missing annotations"
    assert p["importance"] == "Minor"
    assert p["affected_elements"] == 2
    assert "http://ex.org/o#Person" in p["affected"]


def test_parse_empty_response_no_pitfalls():
    empty_xml = '<?xml version="1.0"?><oops:OOPSResponse xmlns:oops="http://www.oeg-upm.net/oops"></oops:OOPSResponse>'
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
