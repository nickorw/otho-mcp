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
# Generate ontology for a specific story
python otho.py --story-id <STORY_ID>

# Use default story (MusicS)
python otho.py

# Benchmark mode: run all stories N times
python otho.py --benchmark <N>
```

**Options:**
- `--story-id <STORY_ID>`: Story ID to process (default: MusicS)
  - Available: `MusicS`, `HospitalS`, `FestS`
- `--benchmark <N>`: Run all three stories N times for benchmarking

### Output Files
All output files are saved to `data/output/` subdirectories with timestamps:
- `ontologies/{story_id}_ontology_{timestamp}.owl` - Final validated ontology
- `validations/{story_id}_validation_{timestamp}.json` - Validation results (syntax + pitfalls)
- `validations/{story_id}_validation_{timestamp}.xml` - OOPS XML report
- `scratchpads/{story_id}_scratchpad_{timestamp}.json` - Agent's planning and iteration history
- `reviews/{story_id}_review_iter{N}_{timestamp}.json` - Review reports for each iteration

All execution logs are saved to `logs/`:
- `{story_id}_generator_{timestamp}.log` - Generator agent human-readable log
- `{story_id}_generator_{timestamp}.json` - Generator agent structured JSON log
- `{story_id}_validation_{timestamp}.log` - Validation human-readable log
- `{story_id}_validation_{timestamp}.json` - Validation structured JSON log

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

### Dual-Agent Workflow
Otho uses a **generator-reviewer dual-agent** architecture built on LangGraph with an iterative review-refinement loop:

```
get_story_node
    ↓
ontology_generation_agent (initial generation)
    ↓
advisory_review_node (iteration 1)
    ↓
review_routing_node
    ├─→ [< 2 iterations] → ontology_generation_agent (refinement) → advisory_review_node (iteration 2)
    └─→ [≥ 2 iterations] → validate_and_save_node (3-pillar validation) → end_node
```

### Workflow Stages

1. **Story Loading**: Reads competency questions from Excel dataset
2. **Generator Agent**: Dual-mode React agent with 5 specialized tools:
   - `update_scratchpad` - Store planning and progress notes
   - `read_scratchpad` - Review previous decisions
   - `validate_syntax_tool` - RDF/Turtle syntax validation
   - `check_pitfalls_tool` - OOPS pitfall detection
   - `save_ontology_draft` - Save final ontology
3. **Self-Validation Loop**: Agent iterates internally until both syntax and pitfalls pass
4. **Persistent Memory**: AgentWorkspace maintains mutable state across tool calls
5. **Complete Auditability**: All decisions, iterations, and validations logged
6. **Advisory Review**: LLM-based reviewer evaluates the ontology and provides structured JSON feedback with CQ coverage analysis, quality metrics, and prioritized improvement suggestions
7. **Refinement Loop**: Generator agent refines based on review feedback (2 iterations guaranteed)
8. **Final Validation**: 3-pillar validation (syntax, OOPS pitfalls, reasoners)

### Key Features
- ✅ **Full Autonomy**: Agent plans, generates, validates, and iterates independently
- ✅ **Self-Validation**: Uses tools to validate its own work, no external validation loop
- ✅ **Persistent Scratchpad**: Maintains planning notes and iteration history
- ✅ **Comprehensive Logging**: Complete audit trail for research analysis
- ✅ **Automatic Iteration**: Continues until validation passes (max 10 attempts)
- ✅ **Dual-Agent Architecture**: Generator and advisory reviewer working in tandem
- ✅ **2-Iteration Review Loop**: Guaranteed review-refinement cycles for quality assurance
- ✅ **Structured Review Feedback**: JSON reports with coverage scores, quality metrics, and prioritized suggestions
- ✅ **Improvement Tracking**: Delta metrics track quality changes across iterations

## Project Structure
```
src/
├── agents/
│   ├── workspace.py         # AgentWorkspace - mutable state container
│   ├── tools.py             # Validation tools (syntax, pitfalls)
│   └── nodes.py             # StateGraph nodes and workflow logic
├── models/
│   └── requirement_models.py   # Story and CompetencyQuestion models
├── prompts/
│   ├── prompt_manager.py
│   ├── prompts.yaml         # Agent prompts with tool documentation
│   └── owl2_datatype_map.txt   # OWL2 datatype reference
├── reviewers/
│   ├── reviewer.py          # RDFSyntaxReviewer, OopsPitfallReviewer
│   └── reasoner_validator.py   # Reasoner-based validation
└── utils/
    ├── agent_logger.py      # Structured logging
    ├── excel_processor.py   # Dataset loading
    ├── file_handler.py      # File I/O operations
    ├── llm_manager.py       # LLM configuration
    ├── ontology_converter.py # OWL format conversion
    ├── oops_parser.py       # OOPS XML parsing
    ├── timing.py            # Execution timing utilities
    └── validation_logger.py # Validation-specific logging

data/
├── input/                   # Excel datasets with CQs
└── output/
    ├── ontologies/          # Generated .owl files
    ├── reviews/             # Review JSON reports
    ├── scratchpads/         # Agent planning history
    └── validations/         # Validation results

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
