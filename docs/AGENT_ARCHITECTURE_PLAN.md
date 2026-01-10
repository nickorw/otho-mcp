# Otho Agent-Centric Architecture Plan

## Executive Summary

Transform Otho into a **self-validating React agent system** where:
- **Agent autonomy**: React agent decides strategy and self-validates its work
- **Internal iteration**: Agent uses validation tools to iteratively improve until passing
- **Minimal state**: Clean state schema with in-state scratchpad for agent memory
- **Linear workflow**: Simple 4-node graph (load → generate → validate → end)
- **Tool-based validation**: Agent has access to syntax and pitfall checking tools

## Design Philosophy

### Agent Controls Everything
- **Strategy**: Agent decides how to generate the ontology (sequential CQs? all-at-once?)
- **Validation**: Agent validates its own work using tools
- **Iteration**: Agent fixes issues and re-validates internally
- **Completion**: Agent explicitly signals completion via tool

### StateGraph Provides Structure
- Entry point and exit points
- Linear workflow nodes (no complex branching)
- State management for agent memory and output

---

## Current Implementation Status (January 2026)

### ✅ What's Implemented
1. Basic StateGraph with 4 nodes: `get_story` → `generate_owl` → `validate_owl` → `end`
2. React agent integration in `generate_owl_node` (using `create_react_agent`)
3. `generate_ontology` prompt in `prompts.yaml` with scratchpad workflow
4. Validation using RDFSyntaxReviewer and OopsPitfallReviewer
5. File saving with timestamps
6. PromptManager for loading prompts from `prompts.yaml`

### ❌ What Needs Implementation
1. **Tools for React agent** (currently empty list)
2. **Scratchpad state field** (not in OntoAgentState)
3. **Agent uses tools for self-validation** (not implemented yet)
4. **save_ontology_draft tool** (to write final output to state)
5. **Iteration tracking** (agent's validation attempts)
6. **Tool state integration** (tools need to read/write state)

---

## Architecture Overview

### High-Level Workflow

```
┌────────────────────────────────────────────────────────┐
│              StateGraph (Orchestration)                 │
└────────────────────────────────────────────────────────┘

         get_story_node
               ↓
    ┌──────────────────────────────────┐
    │  ontology_generation_agent       │  ← React Agent with 5 Tools
    │  (Self-validating agent)         │     * Plans ontology structure
    │                                  │     * Generates OWL code
    │                                  │     * Validates syntax
    │                                  │     * Checks pitfalls
    │                                  │     * Iterates until valid
    │                                  │     * Saves to state
    └──────────────────────────────────┘
               ↓
       validate_and_save_node
         (Final check & persist)
               ↓
            end_node
               ↓
             END
```

### Key Features
- **4 nodes total** (1 is a self-validating React agent)
- **5 tools** for the agent (scratchpad, validation, save)
- **Linear flow** (agent handles iteration internally)
- **In-state scratchpad** for agent's working memory
- **Explicit completion** via `save_ontology_draft` tool

---

## Implementation Details

### 1. AgentWorkspace Class (Shared Mutable Container)

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class AgentWorkspace:
    """
    Mutable workspace for agent's planning, progress tracking, and output.
    This class instance is shared between the node and tools, enabling
    tools to modify data while respecting LangGraph's immutable state pattern.
    """
    scratchpad: Dict[str, Any] = field(default_factory=dict)
    generated_owl: str = ""
    
    def update_scratchpad(self, key: str, value: Any) -> bool:
        """Update scratchpad entry."""
        self.scratchpad[key] = value
        return True
    
    def get_scratchpad(self, key: str) -> Any:
        """Read scratchpad entry."""
        return self.scratchpad.get(key)
    
    def save_ontology(self, owl_content: str) -> bool:
        """Save ontology to workspace."""
        self.generated_owl = owl_content
        return True
    
    def get_iteration_count(self) -> int:
        """Count iterations from scratchpad."""
        iterations = self.scratchpad.get("iterations", [])
        return len(iterations) if isinstance(iterations, list) else 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Export workspace for JSON serialization."""
        return {
            "scratchpad": self.scratchpad,
            "generated_owl": self.generated_owl,
            "iteration_count": self.get_iteration_count()
        }
```

**Why use a class**:
- **Type safety**: Methods have clear signatures with IDE autocomplete
- **Encapsulation**: Logic lives in the class (e.g., `get_iteration_count()`)
- **Cleaner code**: `workspace.scratchpad` vs `agent_data_ref[0]["scratchpad"]`
- **Extensibility**: Easy to add helper methods
- **Works with LangGraph**: Wrapped in List for state immutability

### 2. State Schema

```python
class OntoAgentState(TypedDict, total=False):
    # Input
    story_id: str
    story_object: Story  # Pydantic model with context and CQs
    
    # Shared mutable workspace (class instance wrapped in list)
    workspace: List[AgentWorkspace]  # [workspace_instance]
    
    # Metadata
    validation_history: List[Dict]  # Track all validation attempts
    iteration_count: int  # How many times agent validated internally
    error_message: str  # For catastrophic failures
```

**Key Points:**
- `workspace`: List containing single AgentWorkspace instance (enables mutation)
- Tools modify `workspace[0]` which is shared across agent execution
- State dict remains immutable (LangGraph requirement)
- Workspace contains both scratchpad and generated_owl
- `story_object`: Keep using Story Pydantic model

---

### 3. Scratchpad Structure & Best Practices

#### Recommended Scratchpad Schema
```python
scratchpad = {
    "plan": {
        "classes": [
            "Person", 
            "Resource", 
            "UserResourceUsage"  # Pivot class
        ],
        "properties": [
            {
                "name": "hasUsage",
                "type": "ObjectProperty",
                "domain": "User",
                "range": "UserResourceUsage"
            }
        ],
        "hierarchy": {
            "Person": ["User", "Admin"],
            "Resource": ["DigitalResource", "PhysicalResource"]
        },
        "reification_nodes": [
            {
                "pivot_class": "UserResourceUsage",
                "connects": ["User", "Resource", "xsd:dateTime"],
                "reason": "Models User-Resource-Time relationship"
            }
        ]
    },
    
    "cq_coverage": {
        "CQ1": "Covered by User and hasName data property",
        "CQ2": "Covered by UserResourceUsage and usedAt property",
        "CQ3": "Covered by Resource and hasType property",
        # ... all 15 CQs must be mapped
    },
    
    "iterations": [
        {
            "iteration": 1,
            "action": "Generated initial ontology",
            "validation_result": {
                "syntax_valid": False,
                "error": "Invalid Turtle syntax on line 45"
            },
            "decision": "Fixing missing prefix declaration"
        },
        {
            "iteration": 2,
            "action": "Fixed syntax, re-validating",
            "validation_result": {
                "syntax_valid": True,
                "pitfalls_found": ["P4", "P7"]
            },
            "decision": "Addressing P4 (unconnected elements) and P7 (missing annotations)"
        },
        {
            "iteration": 3,
            "action": "Fixed pitfalls, final validation",
            "validation_result": {
                "syntax_valid": True,
                "pitfalls_found": []
            },
            "decision": "Validation passed! Saving final version."
        }
    ],
    
    "current_owl_draft": "# Working version of ontology...",
    
    "notes": "Using pivot class pattern for complex relationships. All CQs verified."
}
```

#### Scratchpad Best Practices
1. **Structured Planning**: Agent must populate `plan` section BEFORE generating code
2. **CQ Verification**: Every CQ must be explicitly mapped to ontology elements
3. **Iteration Tracking**: Each validation attempt logged with decision rationale
4. **Working Drafts**: Agent can store intermediate OWL versions for comparison
5. **Self-Reflection**: Agent documents reasoning to avoid repeating mistakes

---

### 4. StateGraph Nodes

#### Node 1: `get_story_node`
```python
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    """Load story object and initialize workspace."""
    story_id = state.get("story_id", "")
    story = get_story_by_id(story_id)
    
    # Create new AgentWorkspace instance
    workspace = AgentWorkspace()
    
    return {
        **state,
        "story_object": story,
        "workspace": [workspace],  # Wrap in list to deal with react_agent global state access limitations
        "iteration_count": 0,
        "validation_history": []
    }
```

#### Node 2: `ontology_generation_agent` (Core React Agent)
```python
def ontology_generation_agent(state: OntoAgentState) -> OntoAgentState:
    """
    React agent generates and self-validates ontology.
    
    The agent will:
    1. Plan the ontology structure (using update_scratchpad)
    2. Verify CQ coverage (using update_scratchpad)
    3. Generate OWL code directly (not via tool)
    4. Validate syntax (using validate_syntax tool)
    5. Check pitfalls (using check_pitfalls tool)
    6. Iterate and fix issues until validation passes
    7. Save final ontology (using save_ontology_draft tool)
    
    Maximum 10 iterations to prevent infinite loops.
    """
    
    story_object = state.get("story_object")
    story_id = story_object.id if story_object else ""
    
    print(f"\n{'='*60}")
    print(f"Starting React Agent for Story ID: {story_id}")
    print(f"{'='*60}\n")
    
    # Extract story context and competency questions
    story_context = story_object.context if story_object else ""
    competency_questions = story_object.competency_questions or []
    
    # Format competency questions as text
    cq_list = "\n".join([
        f"{i+1}. {cq.question}" 
        for i, cq in enumerate(competency_questions)
    ])
    
    # Get the base prompt from PromptManager
    # This uses the 'generate_ontology' prompt from prompts.yaml
    prompt = prompt_manager.format_prompt(
        "generate_ontology", 
        story_text=story_context, 
        cq_list=cq_list
    )
    
    # Get workspace reference
    workspace = state["workspace"][0]
    
    # Create tools with workspace reference
    tools = create_agent_tools(workspace)
    
    # Get LLM for React agent
    llm = get_gaih_openai_llm(model="gpt-4.1")
    
    # Create React agent
    print("Creating React agent with 5 tools...")
    agent_executor = create_react_agent(llm, tools)
    
    # Invoke agent
    print("Invoking React agent (this may take several minutes)...\n")
    agent_response = agent_executor.invoke({
        "messages": [HumanMessage(content=prompt)]
    })
    
    # Extract results from workspace (agent updated via tools)
    generated_owl = workspace.generated_owl
    scratchpad = workspace.scratchpad
    iteration_count = workspace.get_iteration_count()
    
    # Save full agent interaction for audit
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    agent_log_path = f"data/output/{story_id}_agent_log_{timestamp}.json"
    
    with open(agent_log_path, 'w') as f:
        json.dump({
            "story_id": story_id,
            "timestamp": timestamp,
            "workspace": workspace.to_dict(),
            "message_count": len(agent_response.get("messages", [])),
            "final_owl_length": len(generated_owl)
        }, f, indent=2)
    
    print(f"\n✓ Agent completed")
    print(f"✓ Agent log saved to: {agent_log_path}")
    print(f"✓ Iterations: {iteration_count}")
    
    return {
        **state,
        "workspace": [workspace],  # Pass workspace reference forward
        "iteration_count": iteration_count,
        "error_message": ""
    }


def create_agent_tools(workspace: AgentWorkspace) -> List:
    """
    Create tool instances with access to shared workspace.
    
    Tools modify the workspace object which is shared between the node and agent.
    This pattern allows mutation while respecting LangGraph's immutable state.
    
    Args:
        workspace: AgentWorkspace instance that tools will modify
    """
    
    @tool
    def update_scratchpad(key: str, value: Any) -> Dict[str, bool]:
        """Update agent's scratchpad in workspace."""
        workspace.update_scratchpad(key, value)
        return {"success": True, "key": key}
    
    @tool
    def read_scratchpad(key: str) -> Any:
        """Read from agent's scratchpad in workspace."""
        return workspace.get_scratchpad(key)
    
    @tool
    def save_ontology_draft(owl_content: str, label: str = "draft") -> Dict[str, Any]:
        """Save ontology to workspace."""
        workspace.save_ontology(owl_content)
        return {
            "saved": True,
            "label": label,
            "length": len(owl_content),
            "message": "Ontology saved to workspace"
        }
    
    # Import standalone validation tools (don't need workspace access)
    from src.agents.tools import validate_syntax_tool, check_pitfalls_tool
    
    return [
        update_scratchpad,
        read_scratchpad,
        validate_syntax_tool,
        check_pitfalls_tool,
        save_ontology_draft
    ]
```

#### Node 3: `validate_and_save_node` (Final Check & Persist)
```python
def validate_and_save_node(state: OntoAgentState) -> OntoAgentState:
    """
    Final validation and save to disk.
    
    This is a safety check - the agent should have already validated,
    but we verify once more and save results to files.
    """
    story_id = state.get("story_id", "")
    
    # Extract from workspace
    workspace = state["workspace"][0]
    generated_owl = workspace.generated_owl
    scratchpad = workspace.scratchpad
    
    if not generated_owl:
        print(f"\n✗ ERROR: No ontology generated by agent!")
        return {
            **state,
            "error_message": "Agent did not produce ontology"
        }
    
    print(f"\n{'='*60}")
    print(f"FINAL VALIDATION FOR {story_id}")
    print(f"{'='*60}\n")
    
    # Final syntax check
    print("Running final syntax validation...")
    syntax_result = RDFSyntaxReviewer().review_owl_content(generated_owl)
    syntax_valid = syntax_result == "OK"
    
    # Final pitfall check
    print("Running final OOPS pitfall check...")
    pitfall_reviewer = OopsPitfallReviewer()
    pitfalls = ["2", "3", "4", "5", "6", "7", "8", "10", "11", "12", "13",
               "19", "20", "21", "22", "24", "25", "26", "27", "28", "29"]
    
    pitfall_result = pitfall_reviewer.review_owl_content(
        owl_content=generated_owl,
        pitfalls=pitfalls,
        output_format="XML"
    )
    pitfall_data = parse_oops_response(pitfall_result)
    has_pitfalls = pitfall_data.get("has_pitfalls", False)
    pitfall_count = pitfall_data.get("pitfall_count", 0)
    
    # Save final ontology
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_path = f"data/output/{story_id}_ontology_{timestamp}.owl"
    save_text_file(final_path, generated_owl)
    print(f"✓ Ontology saved to: {final_path}")
    
    # Save validation results
    validation_path = f"data/output/{story_id}_validation_{timestamp}.xml"
    save_text_file(validation_path, pitfall_result)
    print(f"✓ Validation results saved to: {validation_path}")
    
    # Save scratchpad for audit
    scratchpad_path = f"data/output/{story_id}_scratchpad_{timestamp}.json"
    with open(scratchpad_path, 'w') as f:
        json.dump(scratchpad, f, indent=2)
    print(f"✓ Scratchpad saved to: {scratchpad_path}")
    
    # Report results
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Syntax validation: {'✓ PASSED' if syntax_valid else '✗ FAILED'}")
    if not syntax_valid:
        print(f"  Error: {syntax_result}")
    
    print(f"Pitfall check: {'✓ PASSED' if not has_pitfalls else f'✗ Found {pitfall_count} pitfalls'}")
    if has_pitfalls:
        pitfall_codes = [p.get("code", "") for p in pitfall_data.get("pitfalls", [])]
        print(f"  Pitfalls: {', '.join(pitfall_codes)}")
    
    print(f"Agent iterations: {state.get('iteration_count', 0)}")
    print(f"{'='*60}\n")
    
    return {
        **state,
        "validation_history": state.get("validation_history", []) + [{
            "timestamp": timestamp,
            "syntax_valid": syntax_valid,
            "has_pitfalls": has_pitfalls,
            "pitfall_count": pitfall_count,
            "final_check": True
        }]
    }
```

#### Node 4: `end_node` (Unchanged)
```python
def end_node(state: OntoAgentState) -> OntoAgentState:
    """Workflow termination."""
    print(f"\n✓ Workflow complete for story {state.get('story_id', '')}\n")
    return state
```

---

### 5. StateGraph Assembly

```python
from langgraph.graph import StateGraph, END

# Create graph
graph = StateGraph(state_schema=OntoAgentState)

# Add nodes
graph.add_node("get_story", get_story_node)
graph.add_node("ontology_generation_agent", ontology_generation_agent)
graph.add_node("validate_and_save", validate_and_save_node)
graph.add_node("end", end_node)

# Add edges (linear flow - agent handles iteration internally)
graph.set_entry_point("get_story")
graph.add_edge("get_story", "ontology_generation_agent")
graph.add_edge("ontology_generation_agent", "validate_and_save")
graph.add_edge("validate_and_save", "end")
graph.add_edge("end", END)

# Compile
app = graph.compile()
```

**No conditional edges needed** - the agent itself handles validation and iteration internally!

---

### 6. Tool Definitions

**Note**: Tools 1, 2, and 5 are created as closures in `create_agent_tools()` with workspace access. Tools 3 and 4 are standalone functions imported from `src/agents/tools.py`.

#### Tool 1: `update_scratchpad`
```python
from langchain.tools import tool
from typing import Any, Dict

@tool
def update_scratchpad(key: str, value: Any) -> Dict[str, bool]:
    """
    Update agent's persistent working memory (scratchpad).
    
    Use this to track your planning, progress, and decisions.
    Recommended keys: 
    - 'plan': Your ontology structure plan
    - 'cq_coverage': Mapping of CQs to ontology elements
    - 'iterations': List of validation attempts and fixes
    - 'current_owl_draft': Working version of ontology
    - 'notes': Your reasoning and observations
    
    Args:
        key: The scratchpad key to update
        value: The value to store (can be dict, list, string, etc.)
        
    Returns:
        {"success": True, "key": key}
        
    Example:
        update_scratchpad("plan", {
            "classes": ["User", "Resource"],
            "properties": [{"name": "uses", "type": "ObjectProperty"}]
        })
    """
    # Implementation: Updates state["scratchpad"][key] = value
    # This requires tool to have access to state via closure/context
    return {"success": True, "key": key}
```

#### Tool 2: `read_scratchpad`
```python
@tool
def read_scratchpad(key: str) -> Any:
    """
    Read from agent's persistent working memory (scratchpad).
    
    Use this to review your previous plans, decisions, and drafts.
    
    Args:
        key: The scratchpad key to read
        
    Returns:
        The value stored at that key, or None if not found
        
    Example:
        plan = read_scratchpad("plan")
        previous_iterations = read_scratchpad("iterations")
    """
    # Implementation: Returns state["scratchpad"].get(key)
    return None  # Placeholder - actual implementation accesses state
```

#### Tool 3: `validate_syntax`
```python
@tool
def validate_syntax(owl_content: str) -> Dict[str, Any]:
    """
    Validate RDF/Turtle syntax.
    
    Args:
        owl_content: OWL code in Turtle syntax
        
    Returns:
        {"valid": bool, "error": str or None}
    """
    from src.reviewers.reviewer import RDFSyntaxReviewer
    
    try:
        result = RDFSyntaxReviewer().review_owl_content(owl_content)
        return {"valid": result == "OK", "error": None if result == "OK" else result}
    except Exception as e:
        return {"valid": False, "error": str(e)}


#### Tool 4: `check_pitfalls`
```python
@tool
def check_pitfalls(owl_content: str) -> Dict[str, Any]:
    """
    Check for OOPS pitfalls.
    
    Args:
        owl_content: OWL code in Turtle syntax
        
    Returns:
        {"has_pitfalls": bool, "pitfalls": [...], "count": int}
    """
    from src.reviewers.reviewer import OopsPitfallReviewer
    from src.utils.oops_parser import parse_oops_response
    from src.utils.file_handler import save_text_file
    import tempfile
    import os
    
    # Save to temp file for OOPS
    with tempfile.NamedTemporaryFile(mode='w', suffix='.owl', delete=False) as f:
        f.write(owl_content)
        temp_path = f.name
    
    try:
        result = OopsPitfallReviewer().review_owl_file(
            temp_path,
            pitfalls=["2", "3", "4", "5", "6", "7", "8", "10", "11", "12", "13",
                     "19", "20", "21", "22", "24", "25", "26", "27", "28", "29"]
        )
        pitfall_data = parse_oops_response(result)
        return {
            "has_pitfalls": pitfall_data.get("has_pitfalls", False),
            "pitfalls": pitfall_data.get("pitfalls", []),
            "count": pitfall_data.get("pitfall_count", 0)
        }
    finally:
        os.unlink(temp_path)


#### Tool 5: `save_ontology_draft`
```python
@tool
def save_ontology_draft(owl_content: str, label: str = "draft") -> Dict[str, Any]:
    """
    Save current ontology version to state for final output.
    
    Use this when you have a complete, validated ontology ready for final output.
    This writes to the state's 'generated_owl' field, signaling workflow completion.
    
    IMPORTANT: Only call this after BOTH syntax and pitfall validation have passed!
    
    Args:
        owl_content: Complete OWL ontology in Turtle syntax
        label: Description of this version (e.g., "final_validated", "iteration_3")
        
    Returns:
        {
            "saved": True, 
            "label": label, 
            "length": character_count,
            "message": "Ontology saved to workflow state"
        }
        
    Example:
        # After validation passes
        result = save_ontology_draft(my_final_owl, "final_validated")
        print(result["message"])
    """
    # Implementation: Updates state["generated_owl"] = owl_content
    # Also updates validation_history
    return {
        "saved": True,
        "label": label,
        "length": len(owl_content),
        "message": "Ontology saved to workflow state"
    }
```

**5 tools total - clean and focused.**

---

## Directory Structure

```
src/
├── agents/
│   ├── __init__.py
│   ├── workspace.py          # AgentWorkspace class definition
│   ├── tools.py              # Standalone validation tools (validate_syntax, check_pitfalls)
│   └── nodes.py              # StateGraph node implementations with create_agent_tools
│
├── models/
│   └── requirement_models.py # Story, CompetencyQuestion models
│
├── prompts/
│   ├── prompt_manager.py
│   └── prompts.yaml          # Contains generate_ontology prompt
│
├── reviewers/
│   └── reviewer.py           # RDFSyntaxReviewer, OopsPitfallReviewer
│
└── utils/
    ├── excel_processor.py
    ├── file_handler.py
    ├── llm_manager.py
    └── oops_parser.py

otho.py                       # Updated main script with self-validating agent
```

---

## Implementation Steps

### Step 1: Create AgentWorkspace Class
**File**: `src/agents/workspace.py`
- Define `AgentWorkspace` dataclass with methods
- Implement `update_scratchpad`, `get_scratchpad`, `save_ontology`
- Add `get_iteration_count()` and `to_dict()` helpers
- Add type hints and docstrings

### Step 2: Create Standalone Validation Tools
**File**: `src/agents/tools.py`
- Implement `validate_syntax_tool` (wraps RDFSyntaxReviewer)
- Implement `check_pitfalls_tool` (wraps OopsPitfallReviewer)
- These tools are stateless and don't need workspace access
- Tools return structured dicts for agent parsing

### Step 3: Create Node Module
**File**: `src/agents/nodes.py`
- Implement all 4 nodes
- `ontology_generation_agent` creates tools with workspace reference
- Implement `create_agent_tools(workspace)` function
- Uses PromptManager to load prompts from `prompts.yaml`
- Proper error handling and logging

### Step 4: Update Main Script
**File**: `otho.py`
- Import `AgentWorkspace` from `src.agents.workspace`
- Update `OntoAgentState` schema to use `workspace: List[AgentWorkspace]`
- Import node implementations from `src.agents.nodes`
- Update graph assembly
- Add necessary imports (`json`, `datetime`, etc.)

### Step 5: Update Prompt
**File**: `src/prompts/prompts.yaml`

The existing `generate_ontology` prompt needs minor enhancements to align with tool availability:

**Changes needed:**
1. Update STEP 1 to reference actual tool names: `update_scratchpad("plan", {...})`
2. Update STEP 3 to include iterative validation workflow:
   - Call `validate_syntax(owl_content)` for syntax checking
   - Call `check_pitfalls(owl_content)` for OOPS validation
   - Log iterations with `update_scratchpad("iterations", [...])`
   - Continue until both validations pass (max 10 iterations)
3. Update STEP 4 to call `save_ontology_draft(owl_content, "final_validated")`
4. Update TOOLS AVAILABLE section to list all 5 tools:
   - `update_scratchpad(key, value)` - Store planning, progress, iteration history
   - `read_scratchpad(key)` - Review previous decisions
   - `validate_syntax(owl_content)` - Check RDF/Turtle syntax with rdflib
   - `check_pitfalls(owl_content)` - Check for OOPS modeling pitfalls
   - `save_ontology_draft(owl_content, label)` - Save final version to state
5. Add to CRITICAL CONSTRAINTS:
   - "Do not skip validation steps. Iterate until both syntax and pitfalls pass."
   - "Call save_ontology_draft only after validation passes."

**Note:** The base structure and modeling instructions in the existing prompt are excellent and should be preserved. Only the workflow steps and tool references need updating to match the actual tool implementations.

### Step 6: Testing
- Test on MusicS story
- Verify agent generates complete ontology
- Verify validation and correction loop works
- Compare output quality with original workflow

---

## Success Criteria

### Functional Requirements
✅ Complete OWL ontology generated for all 15 CQs  
✅ Valid RDF/Turtle syntax  
✅ OOPS pitfall-free (or max 5 correction attempts)  
✅ Agent demonstrates autonomous decision-making  
✅ Workflow completes end-to-end  

### Quality Metrics
- **Autonomy**: Agent chooses its own generation strategy
- **Validity**: Passes RDF syntax validation
- **Quality**: Passes OOPS pitfall checks
- **Auditability**: Scratchpad saved for inspection

### Performance Targets
- **Generation Time**: ≤ 30 min for 15 CQs
- **Validation Success**: First-pass validation or successful correction within 5 attempts

---

## Risk Mitigation

### Risk 1: Agent Gets Stuck in Loop
**Mitigation**: 
- Hard limit of 5 retry attempts
- Save scratchpad at each step for debugging
- Agent can read its own history to avoid repeating mistakes

### Risk 2: Agent Ignores Some CQs
**Mitigation**: 
- Objective explicitly lists all 15 CQs
- Validation can check if all CQs are addressed (future enhancement)

### Risk 3: Poor Tool Selection
**Mitigation**: 
- Only 5 tools - hard to choose wrong one
- Clear tool descriptions
- Agent's objective guides tool use

### Risk 4: Syntax Errors in Generated OWL
**Mitigation**: 
- `validate_syntax` tool available to agent
- Agent can self-correct during generation phase
- Validation node catches final errors

---

## Comparison: Old vs New

| Aspect | Before (Current) | After (This Plan) |
|--------|------------------|-------------------|
| **Nodes** | 4 nodes | 4 nodes (same structure) |
| **Agent Tools** | None (empty list) | 5 tools |
| **Agent Autonomy** | Low (just generates) | High (plans, validates, iterates) |
| **Validation** | External (separate node) | Internal (agent self-validates) |
| **Iteration** | None | Agent iterates until valid |
| **State Schema** | 4 fields | 5 fields (workspace contains scratchpad+owl) |
| **Output Method** | Parse response | Tool-based (explicit) |
| **Auditability** | Moderate | High (scratchpad + logs) |
| **Workflow** | Linear, single-pass | Linear, agent multi-pass |
| **Prompt Loading** | PromptManager | PromptManager (unchanged) |


---

## Enhanced Validation Strategy (Phase 2)

### Objective
Extend the validation pipeline to provide comprehensive ontology quality assessment through multiple independent validation methods with proper benchmarking.

### Core Concepts

#### 1. Multi-Dimensional Validation

The architecture validates ontologies across three complementary dimensions:

- **Structural Validation**: Syntactic correctness via RDF/Turtle syntax checking
- **Pitfall Detection**: Modeling anti-patterns and common mistakes via OOPS evaluation
- **Logical Consistency**: Reasoning-based validation to detect contradictions and ensure logical coherence via Hermit and Pellet reasoners

This creates a **three-pillar validation approach**: syntax → pitfalls → reasoning consistency.

Each dimension addresses different aspects of ontology quality:
- Syntax ensures the ontology is machine-readable
- Pitfalls identify design flaws and best practice violations
- Reasoning verifies logical coherence and detects contradictions

#### 2. State Isolation Principle

When multiple validation tools operate on the same ontology, especially reasoning engines that load and process ontological structures, there's a risk of state contamination between validators. The architecture enforces **strict state isolation** where:

- Each validator operates in its own isolated context
- No shared state or memory between validation runs
- Complete cleanup after each validation completes
- No side effects that could influence subsequent validators

This is particularly critical for reasoning engines (Hermit, Pellet) which maintain internal representations of the ontology. State isolation is achieved through:
- Creating separate instances for each validator
- Explicit resource cleanup and garbage collection
- Sequential (not parallel) execution to prevent resource conflicts
- Optional process-level isolation for maximum safety

#### 3. Comprehensive Benchmarking

Each ontology generation produces a **benchmark report** capturing:

- **Performance Metrics**: Execution time for each validator
- **Quality Metrics**: Pass/fail status, issue counts, consistency check results
- **Diagnostic Data**: Specific errors, warnings, or inconsistencies found by each validator
- **Metadata**: Timestamp, retry attempt number, story identifier

This enables:
- Comparison across different ontologies and domains
- Tracking quality improvements through retry iterations
- Performance analysis of validation tools
- Complete audit trail for research reproducibility
- Identification of validation bottlenecks

### Architectural Impact

#### Modified Components

**validate_combined_node**: 
- Expands from single-method (OOPS) to three-method validation
- Sequences validators: syntax → OOPS → Hermit → Pellet
- Aggregates results into unified validation report
- Generates benchmark JSON file for each validation run

**Validation Result Structure**: 
- Enhanced state object captures results from all three validators
- Includes individual validator status and aggregate validation decision
- Preserves detailed diagnostic information for debugging

**Decision Logic**: 
- Validation success requires all three validators to pass
- Configurable strictness levels (e.g., allow minor pitfalls, require reasoning consistency)
- Clear criteria for triggering retry via agent_fix_pitfalls

#### New Capabilities

- **Reasoning-based Consistency Checking**: Integration with Owlready2 library for Hermit and Pellet reasoner access
- **Multi-validator Benchmark Reports**: Structured JSON output capturing comprehensive validation results
- **Aggregate Benchmarking**: Utilities to summarize validation metrics across multiple stories and iterations

#### Integration Points

- **Owlready2 Library**: Python interface to OWL reasoners (Hermit, Pellet)
- **File-based Validation**: Reasoners require file input; temporary files created as needed
- **Benchmark Output**: JSON format for programmatic analysis and aggregation
- **Existing Reviewers**: Reuses RDFSyntaxReviewer and OopsPitfallReviewer infrastructure

### Design Principles

1. **Independence**: Each validator is truly independent - failure in one doesn't prevent execution of others
2. **Clarity**: Benchmark results clearly distinguish between different validation dimensions
3. **Extensibility**: Design allows adding new validators without restructuring the pipeline
4. **Auditability**: Complete validation history preserved for each ontology generation attempt
5. **Performance**: Sequential validation with proper cleanup prevents resource exhaustion

### Success Criteria

**Functional Requirements**:
- All three validators run successfully on generated ontologies
- No state leakage between reasoner executions (verified through repeated runs)
- Benchmark reports generated for every validation attempt
- Validation results are reproducible across multiple runs

**Quality Metrics**:
- Each validator produces actionable diagnostic information
- Benchmark data enables performance comparison across runs
- State isolation prevents false positives/negatives from contamination

**Integration Requirements**:
- Seamless integration with existing StateGraph validation flow
- No disruption to retry logic or agent_fix_pitfalls workflow
- Backward compatible with existing ontology output format

### Expected Outcomes

This enhancement transforms validation from a single-dimensional check into a comprehensive quality assessment framework that:

1. **Increases Confidence**: Multiple independent validators provide higher assurance of ontology quality
2. **Enables Research**: Benchmark data supports comparative analysis across methods and domains
3. **Improves Debugging**: Detailed diagnostic information from three perspectives aids issue resolution
4. **Maintains Performance**: Proper state management prevents resource leaks and slowdowns

---

## Future Enhancements (Phase 3+)

### Phase 3: Enhanced Agent Capabilities
- Agent can request domain-specific examples
- Agent can query ontology design patterns
- Agent provides reasoning for its decisions
- Agent analyzes benchmark trends to optimize generation strategy

### Phase 4: Multi-Agent Collaboration
- Separate agents for generation vs validation
- Peer review between agents
- Collaborative ontology refinement
- Validation agent provides targeted fix suggestions

### Phase 5: Meta-Learning
- Agent learns from previous successful runs
- Adapts strategy based on story domain
- Self-improves prompting techniques
- Learns from validation patterns across datasets

---

## Implementation Notes

### Tool/State Integration Pattern

**The Challenge**: LangGraph requires immutable state (nodes return new state dicts), but tools need to modify shared data (scratchpad, generated_owl).

**The Solution**: Mutable container pattern
- Create `AgentWorkspace` class instance
- Wrap in List and store in state: `workspace: List[AgentWorkspace]`
- Pass workspace reference to tools via `create_agent_tools(workspace)`
- Tools modify `workspace` object (mutable)
- State dict remains immutable (contains workspace reference)

**Why This Works**:
- The workspace **object** is mutable (Python class instance)
- The state **dict** is immutable (new dict returned each time)
- Tools share the workspace reference across agent execution
- LangGraph's state management is satisfied

**Alternatives Considered**:
- Direct state mutation: ❌ Breaks LangGraph's immutability
- Parse agent output: ❌ Agent can't use scratchpad interactively
- LangGraph reducers: ❌ Overly complex for this use case
- List[Dict]: ✅ Works but less ergonomic than class

---

## Validation Checklist

Before implementation:
- [x] Architecture balances structure with autonomy
- [x] Tools are minimal but sufficient
- [x] Agent objectives are clear and achievable
- [x] StateGraph flow is logical
- [x] Success criteria are measurable
- [x] Risks are identified and mitigated
- [x] Timeline is realistic
- [x] Tool/state integration pattern is sound (AgentWorkspace class)

## Notes

- **Core Innovation**: Self-validating agent that uses tools to iteratively improve its work
- **State Management**: In-state scratchpad for persistent agent memory
- **Output Method**: Tool-based (explicit `save_ontology_draft` call)
- **Workflow**: Linear graph, agent handles internal iteration
- **Validation**: Agent-driven with tool access to validators
- **Prompt Loading**: Uses PromptManager to load from `prompts.yaml`
- **Auditability**: Complete scratchpad + agent logs for analysis

---

**Document Version**: 3.0  
**Date**: January 3, 2026  
**Status**: Ready for Implementation  
**Architecture**: Self-Validating React Agent with Linear StateGraph
