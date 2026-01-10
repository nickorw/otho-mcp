# Otho

Research Project Proposal - Otho

## Vision
The best LLM and AI Agent-based OWL ontology generator for business domains.

## Objectives
- Surpass the state-of-the-art in OWL ontology generation for business domains
- Match current overall state-of-the-art

## Hypothesis
The concurrent use of cutting-edge LLMs combined with AI Agents and human-in-the-loop enables improvement of the ontology engineering process beyond the competition.

## Definitions

### Technology
- **Python**: Agility, widely available AI libraries, course requirement
- **LangGraph as agent framework**: LangGraph enables well-defined agent workflow definitions while allowing customization flexibility with broad community support and maturity
- **RDF/OWL as Knowledge Graph technology**: Interest requirement, industry usage
- **Gemini Flash 2.0 as LLM**: Availability for the researcher and performance
- **Blazegraph as Triple Store DB** (if needed)

## Research Project Stages
1. Exploratory research in search engines for similar cases
2. Identification of competing experiments
3. Identification of benchmarks
4. Validation of project objective
5. Preliminary system design
6. Implementation execution and step recording

## Development Project Stages

### Generate Valid OWL Ontologies through LLM
1. Generate with prompt via chat
2. Generate through Python application via API
3. Generate through LangGraph Agent
4. Generate through LangGraph multi-agent application
5. Generate via chat with prompt and text document containing context/Competency Questions (CQs)
6. Generate through LangGraph application with prompt and text document containing context/Competency Questions (CQs)
7. **Extra**: Generate valid OWL ontologies using LLM through LangGraph multi-agent application with added generic business context
8. **Extra**: Collaborative agents (role-playing)

## Bi-modal Evaluation
The evaluation should be bi-modal, implementing automated evaluations where feasible and using experts for qualitative evaluation where automated options face difficulties. Automated evaluations are important for scalability of the evaluation process and enrichment of research results.

### Technical and Intrinsic Evaluation:
- **Logical Consistency**: Automated? (e.g., HermiT, Pellet, FaCT++)
- **Completeness**: Agentic Recursion? Gold ontologies
- **RDF + OWL Syntax**: Available libraries for validation
- **Frameworks**: OQuaRE (Ontology Quality Re-engineering) / OOPS! (Ontology Pitfall Scanner)
- **Evaluation metrics for framework sub-tasks on benchmark datasets**: Precision, Recall, F1
- **Depth and structural complexity**: Class hierarchy depth, number of properties created, interconnection density

### External and Qualitative Evaluation (by Experts)
Consider conducting a comparative study between role-playing agents versus human experts:
- Semantic precision
- Modeling choices
- Usability
- Completeness in implicit requirements

### References
GitHub Saeedizade et al. ESWC 2024: https://github.com/LiUSemWeb/LLMs4OntologyDev-ESWC2024?tab=readme-ov-file

## Usage

### Basic Usage
```bash
python otho.py --story-id MusicS
```

Generates a complete OWL ontology for all 15 competency questions (CQs) using an autonomous React agent that:
- Plans its approach using a persistent scratchpad
- Generates OWL ontology code
- Self-validates syntax using RDFlib
- Checks for pitfalls using OOPS scanner
- Iterates automatically until validation passes (up to 10 iterations)
- Saves the final validated ontology

### Available Story IDs
- `MusicS` - Music streaming domain
- `HospitalS` - Hospital management domain
- `FestS` - Festival organization domain

### Command-Line Options
```bash
python otho.py --story-id <STORY_ID>
```

**Options:**
- `--story-id`: Story ID to process (default: MusicS)

### Output Files
All output files are saved to `data/output/` with timestamps:
- `{story_id}_ontology_{timestamp}.owl` - Final validated ontology
- `{story_id}_validation_{timestamp}.json` - Validation results (syntax + pitfalls)
- `{story_id}_validation_{timestamp}.xml` - OOPS XML report
- `{story_id}_scratchpad_{timestamp}.json` - Agent's planning and iteration history

All execution logs are saved to `logs/`:
- `{story_id}_agent_{timestamp}.log` - Human-readable log
- `{story_id}_agent_{timestamp}.json` - Structured JSON log

## Environment Setup

### OOPS Pitfall Scanner
1. Run Docker container:
   ```bash
   docker run -p 80:8080 mpovedavillalon/oops:v2
   ```

2. Download and mount WordNet, then run:
   ```bash
   docker run -v ./WordNet:/usr/local/tomcat/WordNet -p 80:8080 mpovedavillalon/oops:v2
   ```

3. Access the scanner at: http://localhost/OOPS/

## Architecture

### Agent Workflow
Otho uses a **self-validating React agent** architecture built on LangGraph:

1. **Story Loading**: Reads competency questions from Excel dataset
2. **Autonomous Generation**: React agent with 5 specialized tools:
   - `update_scratchpad` - Store planning and progress notes
   - `read_scratchpad` - Review previous decisions
   - `validate_syntax_tool` - RDF/Turtle syntax validation
   - `check_pitfalls_tool` - OOPS pitfall detection
   - `save_ontology_draft` - Save final ontology
3. **Self-Validation Loop**: Agent iterates internally until both syntax and pitfalls pass
4. **Persistent Memory**: AgentWorkspace maintains mutable state across tool calls
5. **Complete Auditability**: All decisions, iterations, and validations logged

### Key Features
- ✅ **Full Autonomy**: Agent plans, generates, validates, and iterates independently
- ✅ **Self-Validation**: Uses tools to validate its own work, no external validation loop
- ✅ **Persistent Scratchpad**: Maintains planning notes and iteration history
- ✅ **Comprehensive Logging**: Complete audit trail for research analysis
- ✅ **Automatic Iteration**: Continues until validation passes (max 10 attempts)

For detailed architecture documentation, see `docs/AGENT_ARCHITECTURE_PLAN.md` and `docs/IMPLEMENTATION_SUMMARY.md`.

## Project Structure
```
src/
├── agents/
│   ├── workspace.py         # AgentWorkspace - mutable state container
│   ├── tools.py             # Validation tools (syntax, pitfalls)
│   └── nodes.py             # StateGraph nodes (4 nodes)
├── models/
│   └── requirement_models.py   # Story and CompetencyQuestion models
├── prompts/
│   ├── prompt_manager.py
│   └── prompts.yaml         # Agent prompts with tool documentation
├── reviewers/
│   └── reviewer.py          # RDFSyntaxReviewer, OopsPitfallReviewer
└── utils/
    ├── agent_logger.py      # Structured logging
    ├── excel_processor.py   # Dataset loading
    ├── file_handler.py      # File I/O operations
    ├── llm_manager.py       # LLM configuration
    ├── ontology_converter.py # OWL format conversion
    └── oops_parser.py       # OOPS XML parsing

data/
├── input/                   # Excel datasets with CQs
└── output/                  # Generated ontologies and validation results

docs/                        # Architecture and implementation documentation
logs/                        # Agent execution logs
tests/                       # Unit and integration tests

otho.py                      # Main entry point with LangGraph workflow
```

## Installation

### Prerequisites
- Python 3.10+
- Docker (for OOPS Pitfall Scanner)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/nickorw/Otho.git
   cd Otho
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (create `.env` file):
   ```bash
   GOOGLE_API_KEY=your_gemini_api_key
   ```

4. Start OOPS Pitfall Scanner (required):
   ```bash
   docker run -p 80:8080 mpovedavillalon/oops:v2
   ```

## Requirements
See `requirements.txt` for complete list of Python dependencies. Main dependencies:
- `langgraph` - Agent workflow framework
- `langchain` - LLM integration
- `rdflib` - RDF/OWL parsing and validation
- `openpyxl` - Excel file processing
- `google-generativeai` - Gemini API client
