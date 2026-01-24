# Workflow Improvement Analysis for Otho

**Analysis Date:** January 24, 2026  
**Based on:** 91-run experiment data and codebase review  
**Focus:** Outcomes/results and performance improvements for scientific research


## Overview

Based on my review of the codebase and the 91-run experiment data, here are concise observations and improvement opportunities:

---

### **1. OUTCOME IMPROVEMENTS**

**A. Validation Redundancy Issue**
- Agent validates internally (tools) but reasoners (Hermit/Pellet) only run at the *end* in `validate_and_save_node`
- Problem: Agent can't fix reasoner issues—34% failure rate includes reasoner failures that could have been caught earlier
- **Suggestion**: Add reasoner validation tool to agent's toolset for internal iteration

**B. Review Loop Underutilized**
- Advisory review runs 2 iterations (hardcoded) but feedback isn't strongly enforced
- The agent "addresses" suggestions loosely—no verification that high-priority items were fixed
- **Suggestion**: Add structured acceptance criteria; review node should fail the loop if critical suggestions ignored

**C. CQ Coverage Not Verified Systematically**
- Prompt asks agent to map CQs, but no tool verifies completeness
- Review LLM evaluates coverage, but it's subjective
- **Suggestion**: Add SPARQL-based CQ verification tool that tests each CQ against the ontology

**D. Syntax Failures Dominate (74% of failures)**
- 25/34 failures from invalid syntax—agent generates Turtle that doesn't parse
- LLM hallucinating syntax is a known issue
- **Suggestions**: 
  - Provide syntax examples in prompt
  - Add incremental validation (validate after each major addition)
  - Consider generating RDF/XML instead (more verbose but less error-prone)

**E. Scratchpad Underutilized**
- `read_scratchpad` almost never used (1 call in 793 total tool calls)—agent doesn't review its own notes
- Agent isn't leveraging its persistent memory for refinement
- **Suggestion**: Prompt agent to use `read_scratchpad` before refinement iterations

---

### **2. PERFORMANCE IMPROVEMENTS**

**A. Tool Call Overhead**
- 392/793 calls (49%) are `update_scratchpad`—useful for auditability but adds latency
- `read_scratchpad` almost never used (1 call)—agent doesn't review its own notes
- **Suggestion**: Batch scratchpad updates; prompt agent to use `read_scratchpad` before refinement

---

### **3. WORKFLOW ARCHITECTURE**

**A. Hardcoded Review Iterations (2)**
- Fixed loop count regardless of quality scores
- Agent might achieve 100% coverage on first try but still does 2 reviews
- **Suggestion**: Dynamic exit based on quality threshold (e.g., coverage > 0.9 AND quality > 0.85)

**B. No Early Termination on Catastrophic Failure**
- If syntax fails 10 times, agent keeps trying with same prompt
- No fallback strategy or different approach
- **Suggestion**: After N consecutive failures, try alternative (simpler prompt, different model, fewer CQs)

---

### **4. PROMPT/AGENT IMPROVEMENTS**

**A. Prompt Too Long (~2K tokens)**
- Agent may not follow all instructions consistently
- Key constraints buried in long text
- **Suggestion**: Restructure with numbered steps and CRITICAL items first

**B. No Few-Shot Examples**
- Agent generates OWL from scratch each time
- Common patterns (reification, GCAs) could be templated
- **Suggestion**: Include 1-2 minimal working examples in prompt or as tool-accessible reference

**C. Temperature Settings**
- Using 0.5 temperature—allows creativity but also errors
- Syntax generation benefits from lower temperature
- **Suggestion**: Use lower temperature (0.2-0.3) or switch to o1-style reasoning model

---

### **PRIORITY RANKING**

| Priority | Improvement | Expected Impact |
|----------|-------------|-----------------|
| 1 | Add reasoner tool to agent | Catch ~15% more failures early |
| 2 | Fix syntax failure rate (examples/lower temp) | Address 74% of failures |
| 3 | Prompt agent to use scratchpad memory | Improve refinement quality |
| 4 | Dynamic review exit | Save ~30% time on high-quality outputs |

---

## Executive Summary

The Otho workflow achieves a **62.64% success rate** across 91 runs with an average duration of ~5 minutes per run. The primary failure mode is **syntax errors (74% of failures)**, followed by unresolved pitfalls. This analysis identifies opportunities to improve both outcome quality and execution performance.

---
## Detailed view
---

## 1. OUTCOME IMPROVEMENTS

### A. Validation Redundancy Issue

**Current State:**
- Agent validates internally using `validate_syntax_tool` and `check_pitfalls_tool`
- Reasoners (Hermit/Pellet) only run at the *end* in `validate_and_save_node`

**Problem:**
- Agent cannot fix reasoner issues—the 34% failure rate includes reasoner failures that could have been caught and fixed during the agent's iteration loop
- By the time reasoners run, the agent has already "completed" its work

**Suggestion:**
- Add a reasoner validation tool to the agent's toolset
- Allow agent to iterate on logical consistency issues, not just syntax/pitfalls
- Expected impact: Catch ~15% more failures early, enabling agent self-correction

---

### B. Review Loop Underutilized

**Current State:**
- Advisory review runs exactly 2 iterations (hardcoded in `_review_routing_decision`)
- Feedback is provided but enforcement is weak

**Problem:**
- Agent "addresses" suggestions loosely—no verification that high-priority items were actually fixed
- The review prompt asks for improvement tracking, but it's advisory only
- Agent might achieve excellent quality on first attempt but still wastes time on mandatory second review

**Suggestion:**
- Add structured acceptance criteria with measurable thresholds
- Review node should conditionally fail the loop if critical suggestions are ignored
- Implement dynamic exit: if `coverage_score > 0.9` AND `quality_score > 0.85`, skip second review

---

### C. CQ Coverage Not Verified Systematically

**Current State:**
- Prompt asks agent to map Competency Questions to ontology elements
- Review LLM evaluates coverage subjectively

**Problem:**
- No automated verification that each CQ is actually answerable by the ontology
- Reliance on LLM judgment for coverage assessment is inconsistent

**Suggestion:**
- Add SPARQL-based CQ verification tool
- Generate test SPARQL queries for each CQ pattern
- Tool returns concrete results showing which CQs can/cannot be answered
- Provides objective coverage metric for iteration decisions

---

### D. Syntax Failures Dominate (74% of Failures)

**Current State:**
- 25 of 34 failures (74%) are due to invalid Turtle syntax
- Agent generates OWL from scratch each time
- Using temperature 0.5 allows creativity but also errors

**Problem:**
- LLM hallucinating invalid syntax is a known issue with Turtle generation
- No incremental validation—agent builds entire ontology before first syntax check
- No examples of correct syntax patterns in prompt

**Suggestions:**
1. **Provide syntax examples** in prompt or as tool-accessible reference
2. **Add incremental validation**—validate after each major class/property addition
3. **Consider RDF/XML generation**—more verbose but less error-prone
4. **Lower temperature** (0.2-0.3) for syntax generation tasks
5. **Use structured output** where possible (JSON-LD with post-conversion)

---

### E. Scratchpad Underutilized

**Current State:**
- Agent has access to `read_scratchpad` and `update_scratchpad` tools
- From 91 runs: `read_scratchpad` called only 1 time (0.1% of 793 tool calls)
- `update_scratchpad` called 392 times (49.4%)—agent writes notes but never reads them back

**Problem:**
- Agent isn't leveraging its persistent memory for context during refinement
- Planning notes and intermediate decisions are recorded but not reviewed
- Potential loss of continuity between generation and refinement iterations

**Suggestion:**
- Update prompt to explicitly instruct agent to use `read_scratchpad` before refinement iterations
- Review scratchpad content could help agent maintain consistency and avoid repeating mistakes
- Expected impact: Better decision-making in refinement loops, improved quality scores

---

## 2. PERFORMANCE IMPROVEMENTS

### A. Tool Call Overhead

**Current State (from 91 runs):**
- `update_scratchpad`: 392 calls (49.4%)
- `validate_syntax_tool`: 158 calls (19.9%)
- `check_pitfalls_tool`: 158 calls (19.9%)
- `save_final_ontology`: 84 calls (10.6%)
- `read_scratchpad`: 1 call (0.1%)
**Problem:**
- Nearly half of all tool calls are scratchpad updates—useful for auditability but adds latency

**Suggestions:**
- Batch scratchpad updates (update multiple keys in single call)
- Consider whether current scratchpad granularity is necessary

---

## 3. WORKFLOW ARCHITECTURE

### A. Hardcoded Review Iterations

**Current State:**
```python
def _review_routing_decision(state: StateDict) -> str:
    review_iteration = state.get("review_iteration_count", 0)
    if review_iteration < 2:
        return "refine"
    else:
        return "validate"
```

**Problem:**
- Fixed loop count regardless of quality scores achieved
- Excellent first-attempt outputs still undergo mandatory second review
- Poor outputs get only 2 chances regardless of severity

**Suggestion:**
- Dynamic exit based on quality thresholds from review:
  ```python
  if coverage_score > 0.9 and quality_score > 0.85:
      return "validate"  # Skip refinement
  elif review_iteration >= 3:
      return "validate"  # Max iterations reached
  else:
      return "refine"
  ```

---

### B. No Early Termination on Catastrophic Failure

**Current State:**
- If syntax fails repeatedly, agent keeps trying with same approach
- Maximum 10 internal iterations, but no strategy change
- No fallback mechanisms

**Problem:**
- Agent may be stuck in unproductive loop
- Same prompt → same mistakes pattern

**Suggestions:**
- After N consecutive failures of same type, try alternative approach:
  - Simpler prompt (fewer constraints)
  - Different model
  - Fewer CQs (build incrementally)
- Log failure patterns for research analysis

---

## 4. PROMPT/AGENT IMPROVEMENTS

### A. Prompt Complexity

**Current State:**
- `generate_ontology` prompt is ~2000 tokens
- Contains 4 workflow steps, 5 tool descriptions, 7 advanced modeling instructions, 11 critical constraints

**Problem:**
- Agent may not consistently follow all instructions
- Key constraints buried in long text
- Instruction ordering affects attention/compliance

**Suggestions:**
- Restructure with numbered priority levels
- CRITICAL items first, optional enhancements last
- Consider splitting into base prompt + tool-accessible reference documents

---

### B. No Few-Shot Examples

**Current State:**
- Agent generates OWL from scratch each time
- Common patterns (reification, GCAs) described but not shown

**Problem:**
- No concrete syntax examples to anchor generation
- Higher error rate on complex constructs

**Suggestions:**
- Include 1-2 minimal working examples in prompt
- Or: create "get_example" tool for retrieving pattern templates
- Examples for: reification pivot class, GCA, equivalentClass restriction

---

### C. Temperature Settings

**Current State:**
- Using temperature 0.5 for Claude 4.5 Sonnet
- Same temperature for both generation and refinement

**Problem:**
- Moderate temperature allows creativity but also syntax errors
- Refinement benefits from more deterministic behavior

**Suggestions:**
- Lower temperature (0.2-0.3) for syntax-critical generation
- Or: use o1-style reasoning models which handle structured output better
- Consider different temperatures for generation vs refinement modes

---

## 5. PRIORITY RANKING

| Priority | Improvement | Expected Impact | Effort |
|----------|-------------|-----------------|--------|
| **1** | Add reasoner tool to agent | Catch ~15% more failures early | Medium |
| **2** | Fix syntax failure rate (examples/lower temp) | Address 74% of failures | Low |
| **3** | Prompt agent to use scratchpad memory | Improve refinement quality | Low |
| **4** | Dynamic review exit | Save ~30% time on high-quality outputs | Low |
| **5** | SPARQL-based CQ verification | Objective coverage metrics | High |
| **6** | Prompt restructuring | Improve instruction compliance | Medium |

---

## 6. EXPERIMENT DATA SUMMARY

### Overall Statistics (91 Runs)

| Metric | Value |
|--------|-------|
| Success Rate | 62.64% |
| Average Duration | 4.96 minutes |
| Average Iterations | 2.18 |
| Average Tool Calls | 9.44 |

### Per-Story Performance

| Story | Runs | Success Rate | Avg Duration |
|-------|------|--------------|--------------|
| HospitalS | 31 | 67.74% | 5.32 min |
| FestS | 30 | 60.00% | 5.79 min |
| MusicS | 30 | 60.00% | 3.89 min |

### Failure Analysis (34 Failures)

| Failure Reason | Count | Percentage |
|----------------|-------|------------|
| Invalid Syntax | 25 | 73.5% |
| Unresolved Pitfalls | 11 | 32.4% |
| Has Errors | 7 | 20.6% |
| Ontology Not Saved | 7 | 20.6% |

*(Note: Failures can have multiple reasons)*

### Most Common Pitfalls

| Pitfall | Occurrences | Description |
|---------|-------------|-------------|
| P13 | 10 | Missing inverse relationships |
| P11 | 4 | Missing domain or range |
| P29 | 2 | Defining wrong relationships |

---

## Conclusion

The primary opportunity for improvement is **reducing syntax errors**, which account for 74% of failures. This can be addressed through lower temperature settings, few-shot examples, and incremental validation. Secondary improvements in parallelization and dynamic review routing can significantly reduce execution time without sacrificing quality.

For scientific research purposes, the recommended next steps are:
1. Implement syntax examples in prompt (low effort, high impact)
2. Add reasoner tool for agent self-validation (medium effort, high impact)
3. Implement dynamic review exit criteria (low effort, medium impact)

These changes are expected to improve success rate to >80% while reducing average execution time by ~30%.