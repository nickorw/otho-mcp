# Retrofit Execution Checklist

**Strategy**: Add new nodes, edit existing nodes only to add logging

**Source**: `tri-agent-gen-edifact` (most advanced branch)

---

## 🔴 Main Branch - Full Retrofit

### Setup
```bash
git checkout main
git checkout -b retrofit-main-benchmark
```

### Copy Files
```bash
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
Add 4 fields:
```python
log_timestamp: str
story_start_time: float
story_duration_seconds: float
story_duration_formatted: str
```

#### 3. Update get_story_node
```python
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    # ADD:
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_start_time = time.time()

    # ... existing code ...

    return {
        **state,
        # ... existing fields ...
        "log_timestamp": log_timestamp,
        "story_start_time": story_start_time,
    }
```

#### 4. Edit validate_combined_owl_node

**After** `story_id = state.get("story_id", "")`, **ADD**:
```python
combined_owl = state.get("combined_owl", "")
timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")
validation_logger = ValidationLogger(
    story_id=story_id,
    log_dir="logs",
    timestamp=timestamp
)
validation_logger.log_start(ontology_size=len(combined_owl))
```

**Before** syntax validation call, **ADD**:
```python
syntax_start_time = time.time()
```

**After** syntax validation, **ADD**:
```python
syntax_time_seconds = time.time() - syntax_start_time
syntax_valid = syntax_validation_result == "OK"
validation_logger.log_syntax_validation(
    is_valid=syntax_valid,
    execution_time_seconds=syntax_time_seconds,
    error=None if syntax_valid else syntax_validation_result,
)
```

**Before** OOPS validation call, **ADD**:
```python
oops_start_time = time.time()
```

**After** OOPS validation, **REPLACE** the pitfall_data parsing with:
```python
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

**Before** return statement, **ADD**:
```python
validation_logger.save()
log_paths = validation_logger.get_log_paths()
print(f"✓ Validation logs (partial): {log_paths['text_log']}")
```

#### 5. Add new final_reasoner_validation_node

**Insert this entire function** after `validate_combined_owl_node`:

```python
def final_reasoner_validation_node(state: OntoAgentState) -> OntoAgentState:
    """Add reasoner validation (Hermit + Pellet) as Pillar 3."""
    story_id = state.get("story_id", "")
    combined_owl = state.get("combined_owl", "")

    if not combined_owl:
        print("\n⚠ No ontology to validate")
        return state

    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'=' * 60}")
    print(f"FINAL REASONER VALIDATION FOR {story_id}")
    print(f"{'=' * 60}\n")

    # Load existing validation log to append reasoners
    log_json_path = f"logs/{story_id}_validation_{timestamp}.json"

    try:
        if os.path.exists(log_json_path):
            with open(log_json_path, "r") as f:
                existing_log = json.load(f)
                validation_results = existing_log.get("validation_results", {})
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
        print(f"Warning: Could not load existing log: {e}")
        validation_results = {
            "timestamp": timestamp,
            "story_id": story_id,
            "ontology_size_chars": len(combined_owl),
        }

    # Get RDF/XML
    rdfxml_path = "data/output/xml_combined_owl.xml"
    if not os.path.exists(rdfxml_path):
        print(f"⚠ RDF/XML not found - skipping reasoners")
        return state

    print("3️⃣  Reasoning Consistency")
    print("-" * 60)

    # Hermit
    print("  🧠 Hermit reasoner...")
    hermit_validator = HermitReasonerValidator(rdfxml_path=rdfxml_path)
    hermit_result = hermit_validator.validate()
    validation_results["hermit"] = hermit_result

    if hermit_result["is_consistent"]:
        print(f"    ✓ PASSED ({hermit_result['execution_time_seconds']:.3f}s)")
    else:
        print(f"    ✗ FAILED ({hermit_result['execution_time_seconds']:.3f}s)")

    # Pellet
    print("  🧠 Pellet reasoner...")
    pellet_validator = PelletReasonerValidator(rdfxml_path=rdfxml_path)
    pellet_result = pellet_validator.validate()
    validation_results["pellet"] = pellet_result

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

    syntax_valid = validation_results.get("syntax", {}).get("valid", True)
    has_pitfalls = validation_results.get("oops", {}).get("has_pitfalls", False)
    pitfall_count = validation_results.get("oops", {}).get("pitfall_count", 0)

    all_passed = syntax_valid and not has_pitfalls and reasoners_passed

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_seconds": round(total_time, 3),
    }

    # Save JSON
    os.makedirs("data/output/validations", exist_ok=True)
    val_json = f"data/output/validations/{story_id}_validation_{timestamp}.json"
    with open(val_json, "w") as f:
        json.dump(validation_results, f, indent=2)
    print(f"✓ Validation JSON: {val_json}")

    # Re-create logger and save complete logs
    validation_logger = ValidationLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=timestamp
    )
    validation_logger.log_start(ontology_size=len(combined_owl))

    # Re-log syntax and OOPS
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

    # Log reasoners
    validation_logger.log_reasoning_start()
    validation_logger.log_reasoner_validation("Hermit", hermit_result)
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

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

    print(f"✓ Complete logs: {validation_logger.get_log_paths()['text_log']}")
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
    """Create minimal generator log for analyze_logs.py."""
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

Add new nodes:
```python
graph.add_node("final_reasoner_validation", final_reasoner_validation_node)
graph.add_node("create_generator_log", create_generator_log_node)
```

**Modify validate_combined_owl_branch function**:
```python
def validate_combined_owl_branch(state: OntoAgentState) -> str:
    """Branch logic after combined OWL validation"""
    if state.get("combined_validation_ok", False):
        return "final_reasoner_validation"
    else:
        retry_count = state.get("retry_count", 0)
        if retry_count >= 3:
            return "final_reasoner_validation"
        return "correct_owl_pitfalls"
```

Add edges:
```python
graph.add_edge("final_reasoner_validation", "create_generator_log")
graph.add_edge("create_generator_log", "end")
```

### Test

```bash
# Single story
python otho.py --story-id MusicS
ls logs/MusicS_*
cat logs/MusicS_validation_*.json | python -m json.tool | grep -E "hermit|pellet"

# Benchmark
python otho.py --benchmark 2

# Analyze
python analyze_logs.py
cat log_analysis_report.txt
```

### Commit

```bash
git add -A
git commit -m "retrofit: add 3-pillar validation with actual timing"
```

**Time**: 2-2.5 hours

---

## 🟡 Independent_agent_v2 - Add ValidationLogger

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

#### 2. After timestamp creation in validate_and_save_node
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ADD:
validation_logger = ValidationLogger(
    story_id=story_id,
    log_dir="logs",
    timestamp=timestamp
)
validation_logger.log_start(ontology_size=len(generated_owl))
```

#### 3. Convert milliseconds to seconds (4 places)

Find/replace:
- `execution_time_ms` → `execution_time_seconds`
- `int((time.time() - start_time) * 1000)` → `round(time.time() - start_time, 3)`

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
validation_logger.log_pitfall_detection(...)
```

Before reasoners:
```python
validation_logger.log_reasoning_start()
```

After reasoners:
```python
validation_logger.log_reasoner_validation("Hermit", hermit_result)
validation_logger.log_reasoner_validation("Pellet", pellet_result)
```

Before return:
```python
validation_logger.log_summary(...)
validation_logger.save()
```

### Test
```bash
python otho.py --story-id MusicS
python otho.py --benchmark 2
python analyze_logs.py
```

### Commit
```bash
git add -A
git commit -m "retrofit: add ValidationLogger and seconds timing"
```

**Time**: 45 minutes

---

## 🟢 Dual-agent & Tri-agent

### Dual-agent
```bash
git checkout dual-agent-gen-rev
git checkout -b verify-dual-agent-benchmark
git checkout tri-agent-gen-edifact -- analyze_logs.py
git commit -am "update: enhanced analyze_logs"
python otho.py --benchmark 2 && python analyze_logs.py
git tag dual-agent-benchmark-ready
```

### Tri-agent
```bash
git checkout tri-agent-gen-edifact
python otho.py --benchmark 2 && python analyze_logs.py
git tag tri-agent-benchmark-ready
```

**Time**: 20 minutes total

---

## Success Checklist ✅

### Main Branch (retrofit-main-benchmark)
- [x] Branch created and pushed
- [x] Infrastructure files copied
- [x] Code changes completed
- [x] Test passed (MusicS)
- [x] analyze_logs.py verified
- [x] All validators passing (syntax, OOPS, Hermit, Pellet)
- [x] Times in seconds
- [x] Generator + validation logs created
- **Status**: ✅ COMPLETE

### Independent_agent_v2 (retrofit-independent-v2-benchmark)
- [x] Branch created and pushed
- [x] ValidationLogger added
- [x] Timing converted to seconds (4 places)
- [x] Logger calls added (9 locations)
- [x] Test passed (MusicS - 100% validators)
- [x] analyze_logs.py verified (100% success rate)
- [x] Log structure matches tri-agent
- [x] timing.py and reasoner_validator.py from tri-agent
- **Status**: ✅ COMPLETE

### Dual-agent-gen-rev (retrofit-dual-agent-benchmark)
- [x] Branch created and pushed
- [x] analyze_logs.py updated from tri-agent (+23 lines)
- [x] Model set to GPT-4.1 for benchmarking
- [x] Test passed (MusicS - all validators passing)
- [x] analyze_logs.py verified (100% success rate)
- [x] Enhanced log structure (files_saved, story_timing, etc.)
- [x] All infrastructure files identical to tri-agent
- **Status**: ✅ COMPLETE

### Tri-agent-gen-edifact
- [x] Already complete (source of truth)
- [ ] Final verification test needed
- **Status**: ⏳ VERIFY ONLY

---

## Summary

**Completed**: 3 of 4 branches
**Time Spent**: ~2.5 hours
**Remaining**: Tri-agent verification (~10 min)

**All branches configured to use GPT-4.1 for fair benchmarking comparison**

---

**Total Estimated Time**: 3-4 hours
**Actual Progress**: On track, ~85% complete
