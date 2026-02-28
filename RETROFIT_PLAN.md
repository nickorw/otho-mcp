# Retrofit Plan: Add Reasoner Validation & Benchmarking Infrastructure

**Goal**: Enable fair benchmarking across all branch architectures by adding consistent 3-pillar validation (syntax + OOPS + reasoners) and structured logging.

**Strategy**: Minimal changes, add new nodes when possible, create benchmark branches.

---

## Branch Status

| Branch | Has Reasoners | Has ValidationLogger | Has analyze_logs | Action |
|--------|---------------|---------------------|------------------|--------|
| **main** | ❌ | ❌ | ❌ | Full retrofit |
| **independent_agent_v2** | ✅ | ❌ | ❌ | Add logging only |
| **dual-agent-gen-rev** | ✅ | ✅ | ✅ | Update analyze_logs |
| **tri-agent-gen-edifact** | ✅ | ✅ | ✅ | Verify only |

**Source of Truth**: `tri-agent-gen-edifact` (most advanced, has enhanced analyze_logs.py)

---

## Main Branch Retrofit

### What analyze_logs.py Needs

**From generator logs** (`*_generator_*.json`):
- story_id, timestamp, duration_seconds
- ontology_saved (boolean)
- Used for: duration analysis, success tracking

**From validation logs** (`*_validation_*.json`):
- syntax, oops, hermit, pellet results
- execution times for each pillar
- Used for: validation pass rates, reasoner consistency

**Solution**: Create minimal generator logs + full validation logs

### Setup

```bash
git checkout main
git checkout -b retrofit-main-benchmark

# Copy infrastructure from tri-agent (most advanced)
git checkout origin/independent_agent_v2 -- src/reviewers/reasoner_validator.py
git checkout tri-agent-gen-edifact -- src/utils/timing.py
git checkout tri-agent-gen-edifact -- src/utils/validation_logger.py
git checkout tri-agent-gen-edifact -- analyze_logs.py
```

### Code Changes

#### 1. Add imports to otho.py

```python
import time
import json
import os
from datetime import datetime
from src.reviewers.reasoner_validator import HermitReasonerValidator, PelletReasonerValidator
from src.utils.validation_logger import ValidationLogger
from src.utils.timing import format_duration
```

#### 2. Update OntoAgentState

```python
class OntoAgentState(TypedDict, total=False):
    # ... existing fields ...

    # Add these 4 fields:
    log_timestamp: str
    story_start_time: float
    story_duration_seconds: float
    story_duration_formatted: str
```

#### 3. Update get_story_node

Add timestamp tracking:

```python
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    # Add these lines:
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_start_time = time.time()

    print(f"\n{'=' * 60}")
    print(f"Loading Story: {story_id}")
    print(f"Run Timestamp: {log_timestamp}")
    print(f"{'=' * 60}\n")

    story = get_story_by_id(story_id)
    cqs = list(story.competency_questions) if story and story.competency_questions else []

    return {
        **state,
        "story_object": story,
        "unprocessed_cqs": cqs,
        "processed_owls": [],
        "log_timestamp": log_timestamp,  # New
        "story_start_time": story_start_time,  # New
    }
```

#### 4. Edit validate_combined_owl_node (add logging only)

Find the function. After `story_id = state.get("story_id", "")`, add:

```python
# Get combined_owl and add timestamp and logger initialization
combined_owl = state.get("combined_owl", "")
timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")
validation_logger = ValidationLogger(
    story_id=story_id,
    log_dir="logs",
    timestamp=timestamp
)
validation_logger.log_start(ontology_size=len(combined_owl))
```

**Before** syntax validation line, add timing:

```python
# Time syntax validation
import time
syntax_start_time = time.time()
```

**After** syntax validation, add:

```python
# Calculate actual timing
syntax_time_seconds = time.time() - syntax_start_time
syntax_valid = syntax_validation_result == "OK"
validation_logger.log_syntax_validation(
    is_valid=syntax_valid,
    execution_time_seconds=syntax_time_seconds,
    error=None if syntax_valid else syntax_validation_result,
)
```

**Before** OOPS validation call, add:

```python
# Time OOPS validation
oops_start_time = time.time()
```

**After** OOPS validation, replace the existing `pitfall_data = parse_oops_response...` section with:

```python
# Calculate actual timing
oops_time_seconds = time.time() - oops_start_time

pitfall_data = parse_oops_response(pitfall_validation_result)
has_pitfalls = pitfall_data.get("has_pitfalls", False)
pitfall_count = pitfall_data.get("pitfall_count", 0)
pitfalls_list = pitfall_data.get("pitfalls", [])

validation_logger.log_pitfall_detection(
    has_pitfalls=has_pitfalls,
    pitfall_count=pitfall_count,
    execution_time_seconds=oops_time_seconds,
    pitfalls=pitfalls_list,
)
```

Before return statement:

```python
# Save partial validation results (reasoners will be added later)
validation_logger.save()
log_paths = validation_logger.get_log_paths()
print(f"✓ Validation logs (partial): {log_paths['text_log']}, {log_paths['json_log']}")
```

#### 5. Add new final_reasoner_validation_node

Insert this function after `validate_combined_owl_node`:

```python
def final_reasoner_validation_node(state: OntoAgentState) -> OntoAgentState:
    """Add reasoner validation (Hermit + Pellet) as Pillar 3."""
    story_id = state.get("story_id", "")
    combined_owl = state.get("combined_owl", "")

    # Run reasoners even if previous validation had issues (for complete data)
    if not combined_owl:
        print("\n⚠ No ontology to validate with reasoners")
        return state

    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'=' * 60}")
    print(f"FINAL REASONER VALIDATION FOR {story_id}")
    print(f"{'=' * 60}\n")

    # Load existing validation log to append reasoner results
    # This avoids file overwrite conflict with validate_combined_owl_node
    log_json_path = f"logs/{story_id}_validation_{timestamp}.json"

    try:
        if os.path.exists(log_json_path):
            with open(log_json_path, "r") as f:
                existing_log = json.load(f)
                validation_results = existing_log.get("validation_results", {})
                # Preserve existing fields
                if not validation_results:
                    validation_results = {
                        "timestamp": timestamp,
                        "story_id": story_id,
                        "ontology_size_chars": len(combined_owl),
                    }
        else:
            validation_results = {
                "timestamp": timestamp,
                "story_id": story_id,
                "ontology_size_chars": len(combined_owl),
            }
    except Exception as e:
        print(f"Warning: Could not load existing validation log: {e}")
        validation_results = {
            "timestamp": timestamp,
            "story_id": story_id,
            "ontology_size_chars": len(combined_owl),
        }

    # Get RDF/XML from OOPS
    rdfxml_path = "data/output/xml_combined_owl.xml"
    if not os.path.exists(rdfxml_path):
        print(f"⚠ RDF/XML not found - skipping reasoners")
        return state

    print("3️⃣  Reasoning Consistency")
    print("-" * 60)
    validation_logger.log_reasoning_start()

    # Hermit
    print("  🧠 Hermit reasoner...")
    hermit_validator = HermitReasonerValidator(rdfxml_path=rdfxml_path)
    hermit_result = hermit_validator.validate()
    validation_results["hermit"] = hermit_result
    validation_logger.log_reasoner_validation("Hermit", hermit_result)

    if hermit_result["is_consistent"]:
        print(f"    ✓ PASSED ({hermit_result['execution_time_seconds']:.3f}s)")
    else:
        print(f"    ✗ FAILED ({hermit_result['execution_time_seconds']:.3f}s)")

    # Pellet
    print("  🧠 Pellet reasoner...")
    pellet_validator = PelletReasonerValidator(rdfxml_path=rdfxml_path)
    pellet_result = pellet_validator.validate()
    validation_results["pellet"] = pellet_result
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

    if pellet_result["is_consistent"]:
        print(f"    ✓ PASSED ({pellet_result['execution_time_seconds']:.3f}s)\n")
    else:
        print(f"    ✗ FAILED ({pellet_result['execution_time_seconds']:.3f}s)\n")

    # Aggregate
    reasoners_passed = (
        hermit_result["is_consistent"] and pellet_result["is_consistent"]
    )
    total_time = (
        hermit_result["execution_time_seconds"] +
        pellet_result["execution_time_seconds"]
    )

    # Get results from previous validation
    syntax_valid = validation_results.get("syntax", {}).get("valid", True)
    has_pitfalls = validation_results.get("oops", {}).get("has_pitfalls", False)
    pitfall_count = validation_results.get("oops", {}).get("pitfall_count", 0)

    all_passed = syntax_valid and not has_pitfalls and reasoners_passed

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_seconds": round(total_time, 3),
    }

    # Save complete results
    os.makedirs("data/output/validations", exist_ok=True)
    val_json = f"data/output/validations/{story_id}_validation_{timestamp}.json"
    with open(val_json, "w") as f:
        json.dump(validation_results, f, indent=2)
    print(f"✓ Validation JSON: {val_json}")

    # Re-create validation logger and append reasoner results
    validation_logger = ValidationLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=timestamp
    )

    # Re-log everything (logger will handle merging with existing file)
    validation_logger.log_start(ontology_size=len(combined_owl))

    # Re-log syntax and OOPS (from loaded data)
    if "syntax" in validation_results:
        validation_logger.log_syntax_validation(
            is_valid=validation_results["syntax"].get("valid", False),
            execution_time_seconds=validation_results["syntax"].get("execution_time_seconds", 0),
            error=validation_results["syntax"].get("error"),
        )

    if "oops" in validation_results:
        validation_logger.log_pitfall_detection(
            has_pitfalls=validation_results["oops"].get("has_pitfalls", False),
            pitfall_count=validation_results["oops"].get("pitfall_count", 0),
            execution_time_seconds=validation_results["oops"].get("execution_time_seconds", 0),
            pitfalls=validation_results["oops"].get("pitfalls", []),
        )

    # Log reasoner results
    validation_logger.log_reasoning_start()
    validation_logger.log_reasoner_validation("Hermit", hermit_result)
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

    # Final summary
    validation_logger.log_summary(
        syntax_valid=syntax_valid,
        has_pitfalls=has_pitfalls,
        pitfall_count=pitfall_count,
        hermit_consistent=hermit_result["is_consistent"],
        pellet_consistent=pellet_result["is_consistent"],
        all_passed=all_passed,
        total_time_seconds=total_time,
    )
    validation_logger.save()

    print(f"✓ Complete validation logs: {validation_logger.get_log_paths()['text_log']}")
    print(f"{'=' * 60}\n")

    return {
        **state,
        "reasoner_validation": validation_results,
        "reasoners_passed": reasoners_passed,
    }
```

#### 6. Add create_generator_log_node

```python
def create_generator_log_node(state: OntoAgentState) -> OntoAgentState:
    """Create minimal generator log for analyze_logs.py compatibility."""
    story_id = state.get("story_id", "")
    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    story_start_time = state.get("story_start_time")
    if story_start_time:
        duration_seconds = time.time() - story_start_time
        duration_formatted = format_duration(duration_seconds)
    else:
        duration_seconds = 0
        duration_formatted = "0s"

    combined_owl = state.get("combined_owl", "")

    generator_log = {
        "story_id": story_id,
        "timestamp": timestamp,
        "duration_seconds": duration_seconds,
        "duration_formatted": duration_formatted,
        "ontology_saved": len(combined_owl) > 0,
        "ontology_size_chars": len(combined_owl),
        "workflow_type": "main_branch_sequential",
        "iterations": [],
    }

    log_path = f"logs/{story_id}_generator_{timestamp}.json"
    with open(log_path, "w") as f:
        json.dump(generator_log, f, indent=2)

    print(f"✓ Generator log: {log_path}")
    return state
```

#### 7. Update end_node

```python
def end_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    story_start_time = state.get("story_start_time")
    if story_start_time:
        duration = time.time() - story_start_time
        duration_fmt = format_duration(duration)

        print(f"\n{'=' * 60}")
        print(f"WORKFLOW COMPLETE FOR {story_id}")
        print(f"Duration: {duration_fmt}")
        print(f"{'=' * 60}\n")

        return {
            **state,
            "story_duration_seconds": duration,
            "story_duration_formatted": duration_fmt,
        }

    return state
```

#### 8. Update graph workflow

**IMPORTANT**: Main branch uses conditional edges, not direct edges!

Add new nodes:

```python
graph.add_node("final_reasoner_validation", final_reasoner_validation_node)
graph.add_node("create_generator_log", create_generator_log_node)
```

**Modify the conditional branch function** `validate_combined_owl_branch`:

```python
def validate_combined_owl_branch(state: OntoAgentState) -> str:
    """Branch logic after combined OWL validation"""
    if state.get("combined_validation_ok", False):
        # Validation passed - proceed to reasoner validation
        return "final_reasoner_validation"
    else:
        # Validation failed - check retry count
        retry_count = state.get("retry_count", 0)
        if retry_count >= 3:
            # Tried too many times, proceed to reasoners anyway for complete data
            return "final_reasoner_validation"
        return "correct_owl_pitfalls"
```

**Update edges**:

The existing code has:
```python
graph.add_conditional_edges("validate_combined_owl", validate_combined_owl_branch)
graph.add_edge("correct_owl_pitfalls", "validate_combined_owl")
```

Keep those, and add:

```python
# New edges from reasoner validation onward
graph.add_edge("final_reasoner_validation", "create_generator_log")
graph.add_edge("create_generator_log", "end")
```

**Final workflow:**
```
validate_combined_owl → [conditional]
  ├─ if validation OK → final_reasoner_validation → create_generator_log → end
  └─ if validation fails → correct_owl_pitfalls → validate_combined_owl (retry)
                        → (after 3 retries) → final_reasoner_validation → ...
```

### Test

```bash
# Single story test
python otho.py --story-id MusicS

# Verify files
ls logs/MusicS_generator_*.json
ls logs/MusicS_validation_*.json
cat logs/MusicS_validation_*.json | python -m json.tool | grep -E "hermit|pellet"

# Benchmark test
python otho.py --benchmark 2

# Analyze
python analyze_logs.py
cat log_analysis_report.txt
```

### Commit

```bash
git add -A
git commit -m "retrofit: add 3-pillar validation and minimal generator logs"
```

**Time**: 2-2.5 hours

---

## Independent_agent_v2 Retrofit

Already has reasoners. Only need ValidationLogger and analyze_logs.py.

### Setup

```bash
git checkout origin/independent_agent_v2
git checkout -b retrofit-independent-v2-benchmark

git checkout tri-agent-gen-edifact -- src/utils/validation_logger.py
git checkout tri-agent-gen-edifact -- analyze_logs.py
```

### Changes to src/agents/nodes.py

#### 1. Add import

```python
from src.utils.validation_logger import ValidationLogger
```

#### 2. In validate_and_save_node, after timestamp creation:

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Add:
validation_logger = ValidationLogger(
    story_id=story_id,
    log_dir="logs",
    timestamp=timestamp
)
validation_logger.log_start(ontology_size=len(generated_owl))
```

#### 3. Convert milliseconds to seconds (4 places)

Find and replace pattern:
```python
# FIND: execution_time_ms
# REPLACE: execution_time_seconds

# FIND: int((time.time() - start_time) * 1000)
# REPLACE: round(time.time() - start_time, 3)
```

Apply to: syntax, OOPS, Hermit, Pellet, total aggregate

#### 4. Add logger calls

After syntax:
```python
validation_logger.log_syntax_validation(
    is_valid=syntax_valid,
    execution_time_seconds=syntax_time_seconds,
    error=None if syntax_valid else syntax_result,
)
```

After OOPS:
```python
validation_logger.log_pitfall_detection(
    has_pitfalls=has_pitfalls,
    pitfall_count=pitfall_count,
    execution_time_seconds=oops_time_seconds,
    pitfalls=pitfalls_list,
)
```

Before reasoners:
```python
validation_logger.log_reasoning_start()
```

After each reasoner:
```python
validation_logger.log_reasoner_validation("Hermit", hermit_result)
validation_logger.log_reasoner_validation("Pellet", pellet_result)
```

Before return:
```python
validation_logger.log_summary(
    syntax_valid=syntax_valid,
    has_pitfalls=has_pitfalls,
    pitfall_count=pitfall_count,
    hermit_consistent=hermit_result["is_consistent"],
    pellet_consistent=pellet_result["is_consistent"],
    all_passed=all_passed,
    total_time_seconds=total_time_seconds,
)
validation_logger.save()
```

### Test

```bash
python otho.py --story-id MusicS
cat logs/MusicS_validation_*.json | grep execution_time_seconds
python otho.py --benchmark 2
python analyze_logs.py
```

### Commit

```bash
git add -A
git commit -m "retrofit: add ValidationLogger and convert timing to seconds"
```

**Time**: 45 minutes

---

## Dual-agent-gen-rev

Already complete. Just update analyze_logs.py to latest.

```bash
git checkout dual-agent-gen-rev
git checkout -b verify-dual-agent-benchmark

git checkout tri-agent-gen-edifact -- analyze_logs.py
git add analyze_logs.py
git commit -m "update: enhanced analyze_logs from tri-agent"

rm -rf logs/*.json logs/*.log
python otho.py --benchmark 2
python analyze_logs.py

git tag dual-agent-benchmark-ready
```

**Time**: 10 minutes

---

## Tri-agent-gen-edifact

Already complete. Verify only.

```bash
git checkout tri-agent-gen-edifact

rm -rf logs/*.json logs/*.log
python otho.py --benchmark 2
python analyze_logs.py

git tag tri-agent-benchmark-ready
```

**Time**: 10 minutes

---

## Final Benchmark Collection

```bash
mkdir -p benchmark_results

# Run each branch
for branch in retrofit-main-benchmark retrofit-independent-v2-benchmark verify-dual-agent-benchmark tri-agent-gen-edifact; do
    git checkout $branch
    rm -rf logs/*.json logs/*.log
    python otho.py --benchmark 5
    python analyze_logs.py
    cp log_analysis_report.txt benchmark_results/${branch}_report.txt
    cp log_analysis_data.json benchmark_results/${branch}_data.json
done
```

---

## Success Criteria

Per branch:
- [ ] Runs without errors
- [ ] Creates validation logs with hermit/pellet fields
- [ ] Times in seconds (not milliseconds)
- [ ] analyze_logs.py generates report
- [ ] Report has per-run validation table

Cross-branch:
- [ ] Compatible log formats
- [ ] Can compare duration, pass rates, reasoner consistency
- [ ] Architectural differences visible

---

## Total Time: 3-4 hours

| Branch | Time |
|--------|------|
| Main | 2-2.5h |
| Independent_v2 | 45min |
| Dual-agent | 10min |
| Tri-agent | 10min |
