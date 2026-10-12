import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ontologies"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def sample_valid_owl():
    """Return content of first .owl file in fixtures."""
    owl_files = sorted(FIXTURES_DIR.glob("*.owl"))
    if owl_files:
        return owl_files[0].read_text(encoding="utf-8")
    return """@prefix owl: <http://www.w3.org/2002/07/owl#> .
<http://example.org/onto> a owl:Ontology .
"""
