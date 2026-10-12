from rdflib import Graph


def validate_syntax(content: str, format: str = "turtle") -> dict:
    """Validate RDF/OWL syntax using rdflib."""
    if not content or not content.strip():
        return {"valid": False, "error": "Empty content provided", "triple_count": 0}

    g = Graph()
    try:
        g.parse(data=content, format=format)
        return {"valid": True, "error": None, "triple_count": len(g)}
    except Exception as e:
        return {"valid": False, "error": str(e), "triple_count": 0}
