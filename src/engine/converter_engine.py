from rdflib import Graph

SUPPORTED_FORMATS = ["turtle", "xml", "n3", "nt", "json-ld", "pretty-xml"]


def convert_format(content: str, source_format: str, target_format: str) -> str:
    """Convert ontology content between RDF serialization formats."""
    if source_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported source format: {source_format}. Supported: {SUPPORTED_FORMATS}")
    if target_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported target format: {target_format}. Supported: {SUPPORTED_FORMATS}")

    g = Graph()
    g.parse(data=content, format=source_format)
    return g.serialize(format=target_format)
