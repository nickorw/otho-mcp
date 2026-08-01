# OthoMCP

OthoMCP is your plug-n-play suite for OWL ontology validation, incorporating syntax, modeling pitfall and DL validations in a single docker container. It encapsulates OOps Pitfall Scanner, HermiT and Pellet, exposing 9 tools for syntax checking, pitfall detection, consistency reasoning, metrics computation, and format conversion. It is particularly helpful for the validation of LLM-generated ontologies, offering both individual and bulk analysis. All of that while saving you from individual setups or prerequisite management. 

## Prerequisites

Docker Desktop (macOS/Windows) or Docker Engine + Compose (Linux).

## Quick Start

1. Start the server:
   ```bash
   docker compose up -d
   ```
2. Verify it's running:
   ```bash
   curl http://localhost:8000/health   # -> {"status":"ok"}
3. Add it to your MCP client (see [Client Configuration](#client-configuration)), and done. (see [Using It](#using-it)).
   ```

The MCP endpoint is at `http://localhost:8000/mcp`.

## Client Configuration

Add the server to your MCP client's configuration. The exact file and format vary by client, but the entry looks like:

```json
{
  "mcpServers": {
    "otho-mcp": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Restart or reload your client so it picks up the new server. Its 9 tools are then available to whatever agent or interface your client provides.

## Using It

Once configured, drive the tools through your MCP client however it exposes them — typically by asking the client's agent in natural language.

Every tool takes its ontology **one of two ways** — use whichever suits you:

- **A path from your machine** — a file *or* a folder. No uploads or copying; you reference it where it already lives:
  > Validate the ontology at `/Users/you/onto/foo.owl`

  > Run a full validation on the folder `~/ontologies` and give me the OOPs report

- **Plain ontology text** — hand the content directly, with no file involved:
  > Check the syntax of this ontology: `@prefix owl: <...> . :Foo a owl:Class .`

Paths must live under your home directory (see [File & folder paths](#file--folder-paths)); for anything else, pass the content as text instead.

New to the tools? Start with **`validate_all`** for a complete check (syntax + pitfalls + reasoning) of a single file, or **`validate_syntax`** for a fast sanity check. See the [Tools](#tools) table for the full set.

## Tools

| Tool | Description |
|------|-------------|
| `validate_syntax` | Validate RDF/OWL syntax using rdflib |
| `validate_oops` | Detect 22 OOPs modeling anti-patterns with severity levels |
| `validate_reasoning` | Check logical consistency with HermiT/Pellet reasoners |
| `validate_all` | Full validation battery (syntax + OOPs + reasoning) |
| `validate_batch` | Run validators on all ontology files in a folder |
| `oops_report` | Folder-level OOPs report with severity aggregation |
| `ontology_metrics` | Structural metrics: axiom counts, hierarchy, OntoQA, complexity, lexical |
| `convert_format` | Convert between turtle, xml, n3, nt, json-ld |
| `explain_pitfall` | Look up explanation and fix guidance for a pitfall code (P01–P41) |

Every tool accepts its ontology as either a **path from your machine** (a file, or a folder for the batch tools `validate_batch` and `oops_report`) or as **inline text**. See [Using It](#using-it) for examples and [File & folder paths](#file--folder-paths) for how paths are resolved. (The underlying arguments, for programmatic callers, are `file_path` / `folder_path` and `owl_content`.)

### File & folder paths

Your **home directory is mounted into the container**, so you can pass real paths from your system directly — e.g. `/Users/you/onto/foo.owl` (macOS/Linux) or `C:\Users\you\onto\foo.owl` (Windows). Both file paths and folder paths (for `validate_batch` / `oops_report`) work.

- **Scope:** any path *under your home directory* is reachable. Files outside home (other drives, system dirs) are not visible to the container — pass those via `owl_content` instead.
- **Windows:** Docker Desktop usually provides `HOME` automatically. If your paths don't resolve, set `HOST_HOME` in a `.env` file (e.g. `HOST_HOME=C:\Users\you`) so the server knows your home prefix.
- **Read-only:** the mount is read-only; the tools never modify your files.

## Architecture

```
docker compose
└── otho-mcp (Python 3.11 + JDK 11)
    ├── FastMCP server (Streamable HTTP on :8000)
    ├── OOPs pitfall scanner (Tomcat REST on :8080, in-container)
    ├── Engine layer (syntax, oops, reasoner, metrics, converter)
    └── Home directory mounted read-only at /host
```

- **Reasoner isolation:** HermiT/Pellet run in spawned subprocesses with configurable timeout
- **File access:** Your home directory is bind-mounted read-only at `/host`; the server maps incoming host paths (stripping the `HOST_HOME` prefix) into that mount
- **OOPs integration:** Ontologies are converted to RDF/XML and sent to the OOPs REST API

## Development

```bash
# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run server locally (without Docker)
python -m src.server
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST_HOME` | `$HOME` | Host home directory to mount and strip from incoming paths (set to `C:\Users\you` on Windows if needed) |
| `OOPS_URL` | `http://localhost:8080/OOPS/rest` | OOPs service endpoint |
| `REASONER_TIMEOUT` | `120` | Reasoner subprocess timeout (seconds) |
| `HOST_MOUNT_PREFIX` | `/host` | Container-internal mount path |
| `SERVER_HOST` | `0.0.0.0` | Server bind address |
| `SERVER_PORT` | `8000` | Server port |
