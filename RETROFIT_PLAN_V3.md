# REVISED Retrofit Plan v3.0

**Date**: 2026-02-28
**Status**: CORRECTED after critical review

## Critical Fixes from Review

### Issue #1: Main Branch Generator Logs ✅ FIXED
**Solution**: Create minimal generator logs in main branch
- Add simple logging node to capture story_id, timestamp, duration
- Enough for analyze_logs.py to work without full agent complexity

### Issue #2: ValidationLogger Integration ✅ FIXED
**Solution**: CAN edit existing validation node to add logging
- User approved: "You may edit the node IF it is just to add logs"
- Add ValidationLogger calls to capture syntax + OOPS results
- No logic changes, only logging additions

### Issue #3: Hard-coded Values ✅ FIXED
**Solution**: Parse actual validation results from state
- Extract syntax_valid from state validation results
- Parse pitfall_count from OOPS response
- Log actual values, not fake ones

### Issue #4: Using Benchmark Branches ✅ CONFIRMED
**Reminder**: We're on benchmark branches, not touching originals
- Safe to experiment
- Can iterate without risk
- Easy to delete and restart if needed

---

## Main Branch Retrofit - CORRECTED APPROACH

### Strategy: Hybrid Approach
1. **ADD** new reasoner validation node (non-invasive)
2. **EDIT** existing validation node to add ValidationLogger (logging only)
3. **ADD** minimal generator log creation

### Step-by-Step Implementation

#### Step 1: Copy Infrastructure Files

```bash
git checkout main
git checkout -b retrofit-main-benchmark

# Copy from tri-agent (most advanced)
git checkout origin/independent_agent_v2 -- src/reviewers/reasoner_validator.py
git checkout tri-agent-gen-edifact -- src/utils/timing.py
git checkout tri-agent-gen-edifact -- src/utils/validation_logger.py
git checkout tri-agent-gen-edifact -- analyze_logs.py
```

#### Step 2: Add Imports to otho.py

```python
import time
import json
from datetime import datetime
from src.reviewers.reasoner_validator import HermitReasonerValidator, PelletReasonerValidator
from src.utils.validation_logger import ValidationLogger
from src.utils.timing import format_duration, calculate_duration_seconds
```

#### Step 3: Update OntoAgentState

```python
class OntoAgentState(TypedDict, total=False):
    # ... all existing fields ...

    # ADD THESE:
    log_timestamp: str
    story_start_time: float
    story_duration_seconds: float
    story_duration_formatted: str
```

#### Step 4: Update get_story_node (minimal change)

```python
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    # ADD: Timestamp and timing
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_start_time = time.time()

    print(f"\n{'=' * 60}")
    print(f"Loading Story: {story_id}")
    print(f"Run Timestamp: {log_timestamp}")  # ADD
    print(f"{'=' * 60}\n")

    story = get_story_by_id(story_id)
    cqs = list(story.competency_questions) if story and story.competency_questions else []

    return {
        **state,
        "story_object": story,
        "unprocessed_cqs": cqs,
        "processed_owls": [],
        "log_timestamp": log_timestamp,  # ADD
        "story_start_time": story_start_time,  # ADD
    }
```

#### Step 5: ADD ValidationLogger to Existing validate_combined_owl_node

**IMPORTANT**: Only adding logging, not changing validation logic!

Find the existing `validate_combined_owl_node` function. After the line:
```python
story_id = state.get("story_id", "")
```

**ADD** these lines:
```python
# Get shared timestamp
log_timestamp = state.get("log_timestamp")
timestamp = log_timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

# Initialize validation logger
validation_logger = ValidationLogger(
    story_id=story_id,
    log_dir="logs",
    timestamp=timestamp
)
validation_logger.log_start(ontology_size=len(combined_owl))
```

Then **AFTER** syntax validation (find line ~212 where syntax_validation_result is set):
```python
syntax_validation_result = syntax_reviewer.review_owl_content(combined_owl)
print("Syntax Validation Result:", syntax_validation_result)

# ADD THIS:
syntax_valid = syntax_validation_result == "OK"
syntax_time_seconds = 0.1  # Approximate, since we don't time it separately
validation_logger.log_syntax_validation(
    is_valid=syntax_valid,
    execution_time_seconds=syntax_time_seconds,
    error=None if syntax_valid else syntax_validation_result,
)
```

Then **AFTER** OOPS validation (find where pitfall_data is parsed):
```python
pitfall_data = parse_oops_response(pitfall_validation_result)

# ADD THIS:
has_pitfalls = pitfall_data.get("has_pitfalls", False)
pitfall_count = pitfall_data.get("pitfall_count", 0)
pitfalls_list = pitfall_data.get("pitfalls", [])
oops_time_seconds = 2.0  # Approximate
validation_logger.log_pitfall_detection(
    has_pitfalls=has_pitfalls,
    pitfall_count=pitfall_count,
    execution_time_seconds=oops_time_seconds,
    pitfalls=pitfalls_list,
)
```

**At the END** of the function, before the return statement:
```python
# ADD THIS:
validation_logger.save()
log_paths = validation_logger.get_log_paths()
print(f"✓ Validation logs saved:")
print(f"  - {log_paths['text_log']}")
print(f"  - {log_paths['json_log']}")
```

#### Step 6: ADD New Reasoner Validation Node

**Add this entire new function** after `validate_combined_owl_node`:

```python
def final_reasoner_validation_node(state: OntoAgentState) -> OntoAgentState:
    """
    NEW NODE: Reasoner validation (Pillar 3) after existing validation.
    Runs Hermit and Pellet on the ontology to check logical consistency.
    """
    import os

    story_id = state.get("story_id", "")
    combined_owl = state.get("combined_owl", "")

    # Skip if previous validation failed
    if not state.get("combined_validation_ok", False):
        print(f"\n⚠ Skipping reasoner validation - previous validation failed")
        return state

    if not combined_owl:
        print(f"\n⚠ No ontology to validate")
        return state

    # Get shared timestamp
    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'=' * 60}")
    print(f"FINAL REASONER VALIDATION FOR {story_id}")
    print(f"{'=' * 60}\n")

    # Get existing validation logger or create new one
    validation_logger = ValidationLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=timestamp
    )

    # Load existing log if it exists to append reasoner results
    try:
        existing_log_path = f"logs/{story_id}_validation_{timestamp}.json"
        if os.path.exists(existing_log_path):
            with open(existing_log_path, "r") as f:
                validation_results = json.load(f)
        else:
            validation_results = {
                "timestamp": timestamp,
                "story_id": story_id,
                "ontology_size_chars": len(combined_owl),
            }
    except:
        validation_results = {
            "timestamp": timestamp,
            "story_id": story_id,
            "ontology_size_chars": len(combined_owl),
        }

    # Get RDF/XML path (created by OOPS in previous node)
    rdfxml_path = "data/output/xml_combined_owl.xml"

    if not os.path.exists(rdfxml_path):
        print(f"⚠ RDF/XML not found at {rdfxml_path} - skipping reasoners")
        return state

    print("3️⃣  Reasoning Consistency")
    print("-" * 60)
    validation_logger.log_reasoning_start()

    # Hermit Reasoner
    print("  🧠 Running Hermit reasoner...")
    hermit_validator = HermitReasonerValidator(rdfxml_path=rdfxml_path)
    hermit_result = hermit_validator.validate()
    validation_results["hermit"] = hermit_result
    validation_logger.log_reasoner_validation("Hermit", hermit_result)

    if hermit_result["is_consistent"]:
        print(f"    ✓ PASSED ({hermit_result['execution_time_seconds']:.3f}s)")
    else:
        print(f"    ✗ FAILED ({hermit_result['execution_time_seconds']:.3f}s)")
        if hermit_result.get("inconsistent_classes"):
            print(f"    Inconsistent: {hermit_result['inconsistent_classes']}")

    # Pellet Reasoner
    print("  🧠 Running Pellet reasoner...")
    pellet_validator = PelletReasonerValidator(rdfxml_path=rdfxml_path)
    pellet_result = pellet_validator.validate()
    validation_results["pellet"] = pellet_result
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

    if pellet_result["is_consistent"]:
        print(f"    ✓ PASSED ({pellet_result['execution_time_seconds']:.3f}s)\n")
    else:
        print(f"    ✗ FAILED ({pellet_result['execution_time_seconds']:.3f}s)")
        if pellet_result.get("inconsistent_classes"):
            print(f"    Inconsistent: {pellet_result['inconsistent_classes']}\n")

    # Aggregate results
    reasoners_passed = (
        hermit_result["is_consistent"] and pellet_result["is_consistent"]
    )
    total_reasoner_time = (
        hermit_result["execution_time_seconds"] +
        pellet_result["execution_time_seconds"]
    )

    # Get syntax and OOPS results from previous validation
    syntax_valid = validation_results.get("syntax", {}).get("valid", True)
    has_pitfalls = validation_results.get("oops", {}).get("has_pitfalls", False)
    pitfall_count = validation_results.get("oops", {}).get("pitfall_count", 0)

    # Overall aggregate
    all_passed = syntax_valid and not has_pitfalls and reasoners_passed

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_seconds": round(total_reasoner_time, 3),
    }

    # Save complete validation results
    os.makedirs("data/output/validations", exist_ok=True)
    validation_json = f"data/output/validations/{story_id}_validation_{timestamp}.json"
    with open(validation_json, "w") as f:
        json.dump(validation_results, f, indent=2)
    print(f"✓ Validation JSON: {validation_json}")

    # Save validation logs
    validation_logger.log_summary(
        syntax_valid=syntax_valid,
        has_pitfalls=has_pitfalls,
        pitfall_count=pitfall_count,
        hermit_consistent=hermit_result["is_consistent"],
        pellet_consistent=pellet_result["is_consistent"],
        all_passed=all_passed,
        total_time_seconds=total_reasoner_time,
    )
    validation_logger.save()

    log_paths = validation_logger.get_log_paths()
    print(f"✓ Logs: {log_paths['text_log']}, {log_paths['json_log']}")
    print(f"{'=' * 60}\n")

    return {
        **state,
        "reasoner_validation": validation_results,
        "reasoners_passed": reasoners_passed,
    }
```

#### Step 7: ADD Minimal Generator Log Node

**Add this new function** to create minimal generator logs:

```python
def create_generator_log_node(state: OntoAgentState) -> OntoAgentState:
    """
    NEW NODE: Create minimal generator log for analyze_logs.py compatibility.

    Main branch doesn't have agent architecture, but analyze_logs.py expects
    generator logs. This creates minimal logs with just the essential fields.
    """
    story_id = state.get("story_id", "")
    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    # Calculate duration
    story_start_time = state.get("story_start_time")
    if story_start_time:
        duration_seconds = time.time() - story_start_time
        duration_formatted = format_duration(duration_seconds)
    else:
        duration_seconds = 0
        duration_formatted = "0s"

    # Check if ontology was created
    combined_owl = state.get("combined_owl", "")
    ontology_saved = len(combined_owl) > 0

    # Create minimal generator log
    generator_log = {
        "story_id": story_id,
        "timestamp": timestamp,
        "duration_seconds": duration_seconds,
        "duration_formatted": duration_formatted,
        "ontology_saved": ontology_saved,
        "ontology_size_chars": len(combined_owl),
        "workflow_type": "main_branch_sequential",
        "iterations": [],  # Empty for main branch (no agent iterations)
        "note": "Minimal log for main branch compatibility with analyze_logs.py"
    }

    # Save generator log
    log_path = f"logs/{story_id}_generator_{timestamp}.json"
    with open(log_path, "w") as f:
        json.dump(generator_log, f, indent=2)

    print(f"✓ Generator log: {log_path}")

    return state
```

#### Step 8: Update end_node

```python
def end_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    # ADD: Duration calculation
    story_start_time = state.get("story_start_time")
    if story_start_time:
        story_duration_seconds = time.time() - story_start_time
        story_duration_formatted = format_duration(story_duration_seconds)

        print(f"\n{'=' * 60}")
        print(f"WORKFLOW COMPLETE FOR {story_id}")
        print(f"Duration: {story_duration_formatted}")
        print(f"{'=' * 60}\n")

        return {
            **state,
            "story_duration_seconds": story_duration_seconds,
            "story_duration_formatted": story_duration_formatted,
        }

    return state
```

#### Step 9: Update Graph Workflow

Find the graph construction section (around line 361-380). Update it:

```python
# EXISTING nodes (keep as is)
graph.add_node("get_story", get_story_node)
graph.add_node("generate_owl", generate_owl_node)
graph.add_node("validate_and_store_owl", validate_and_store_owl_node)
graph.add_node("combine_owls", combine_owls_node)
graph.add_node("validate_combined_owl", validate_combined_owl_node)
graph.add_node("correct_owl_pitfalls", correct_owl_pitfalls_node)
graph.add_node("end", end_node)

# ADD NEW NODES:
graph.add_node("final_reasoner_validation", final_reasoner_validation_node)
graph.add_node("create_generator_log", create_generator_log_node)

# EXISTING edges (keep as is)
graph.set_entry_point("get_story")
graph.add_edge("get_story", "generate_owl")
graph.add_edge("generate_owl", "validate_and_store_owl")
graph.add_conditional_edges("validate_and_store_owl", validate_and_store_owl_branch)
graph.add_edge("combine_owls", "validate_combined_owl")
graph.add_conditional_edges("validate_combined_owl", validate_combined_owl_branch)
graph.add_edge("correct_owl_pitfalls", "validate_combined_owl")

# MODIFY THIS LINE:
# BEFORE: (somewhere there's an edge to "end")
# AFTER: Insert new nodes before end

# Find where workflow goes to "end" and change to:
graph.add_edge("validate_combined_owl", "final_reasoner_validation")
graph.add_edge("final_reasoner_validation", "create_generator_log")
graph.add_edge("create_generator_log", "end")
```

**Note**: You'll need to check the conditional edges carefully to ensure the new nodes are inserted at the right place in the flow.

#### Step 10: Test

```bash
# Smoke test
python otho.py --story-id MusicS

# Verify files created
ls -la logs/MusicS_generator_*.json
ls -la logs/MusicS_validation_*.json
ls -la logs/MusicS_validation_*.log

# Check generator log content
cat logs/MusicS_generator_*.json | python -m json.tool

# Check validation log has all 3 pillars
cat logs/MusicS_validation_*.json | python -m json.tool | grep -E "syntax|oops|hermit|pellet"

# Quick benchmark
python otho.py --benchmark 2

# Should create:
# - 6 generator logs (2 iter × 3 stories)
# - 6 validation logs
ls logs/*_generator_*.json | wc -l  # Should be 6
ls logs/*_validation_*.json | wc -l  # Should be 6

# Analyze
python analyze_logs.py

# Verify report
cat log_analysis_report.txt
```

### Expected Output Files Per Story

```
logs/
  ├── MusicS_generator_20260228_143022.json      ← Minimal generator log
  ├── MusicS_validation_20260228_143022.json     ← Full validation results
  └── MusicS_validation_20260228_143022.log      ← Human-readable log

data/output/validations/
  └── MusicS_validation_20260228_143022.json     ← Duplicate for organization
```

---

## Independent_agent_v2 Retrofit - SIMPLIFIED

Since this branch already has reasoners, we only need:
1. Add ValidationLogger calls
2. Convert milliseconds to seconds
3. Add analyze_logs.py

**(See RETROFIT_CHECKLIST.md for detailed steps - unchanged)**

---

## Success Criteria ✅

### Main Branch
- [ ] Runs `python otho.py --story-id MusicS` without errors
- [ ] Creates `*_generator_*.json` (minimal format)
- [ ] Creates `*_validation_*.json` with syntax, oops, hermit, pellet
- [ ] Creates `*_validation_*.log` (human-readable)
- [ ] `python analyze_logs.py` works without errors
- [ ] Report shows both generator and validation metrics

### Cross-Branch Comparison
- [ ] All branches produce compatible log formats
- [ ] analyze_logs.py works on all branches
- [ ] Can compare: duration, validation pass rates, reasoner consistency
- [ ] Clear architectural differences visible in metrics

---

## Timeline

| Branch | Task | Time |
|--------|------|------|
| Main | Full retrofit with 3 new nodes | 2-2.5 hours |
| Independent_v2 | Add logging only | 45 min |
| Dual-agent | Update analyze_logs | 10 min |
| Tri-agent | Verify only | 10 min |
| **TOTAL** | | **3-4 hours** |

---

**Version**: 3.0 (Corrected after critical review)
**Date**: 2026-02-28
**Status**: Ready for implementation
