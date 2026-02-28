#!/usr/bin/env python3
"""
Comprehensive analysis of all agent log files from the Otho ontology generation experiments.
Analyzes generator runs and validation runs across 3 stories (FestS, HospitalS, MusicS).
"""

import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from src.utils.timing import calculate_duration_seconds


def load_all_logs(logs_dir="logs"):
    """Load all generator JSON log files."""
    logs = []
    log_files = sorted(Path(logs_dir).glob("*_generator_*.json"))

    if not log_files:
        print(f"Warning: No generator JSON log files found in {logs_dir}")
        return logs

    for log_file in log_files:
        try:
            with open(log_file, "r") as f:
                data = json.load(f)
                data["filename"] = log_file.name
                logs.append(data)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {log_file}: {e}")
        except Exception as e:
            print(f"Error loading {log_file}: {e}")

    return logs


def load_validation_logs(logs_dir="logs"):
    """Load all validation JSON log files."""
    logs = []
    log_files = sorted(Path(logs_dir).glob("*_validation_*.json"))

    if not log_files:
        print(f"Warning: No validation JSON log files found in {logs_dir}")
        return logs

    for log_file in log_files:
        try:
            with open(log_file, "r") as f:
                data = json.load(f)
                data["filename"] = log_file.name
                logs.append(data)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {log_file}: {e}")
        except Exception as e:
            print(f"Error loading {log_file}: {e}")

    return logs


def extract_metrics(log_data):
    """Extract key metrics from a single generator log file."""
    # Handle the nested iterations structure from agent_logger.py
    # The log structure is: { iterations: [ {iteration: 1, metadata: {...}, tool_calls: [...], workspace_state: {...}} ] }
    agent_iterations = log_data.get("iterations", [])

    # Get the last iteration (most recent/final state)
    last_iteration = agent_iterations[-1] if agent_iterations else {}

    # Get metadata from the last iteration
    metadata = last_iteration.get("metadata", {})

    # Get workspace state from the last iteration
    workspace_state = last_iteration.get("workspace_state", {})

    # Aggregate errors from all iterations
    all_errors = []
    for iter_data in agent_iterations:
        all_errors.extend(iter_data.get("errors", []))

    # Get start and end times
    start_time = log_data.get("run_start_time", "") or (
        agent_iterations[0].get("start_time", "") if agent_iterations else ""
    )
    end_time = last_iteration.get("end_time", "") or log_data.get("run_end_time", "")

    metrics = {
        "story_id": log_data.get("story_id", "unknown"),
        "timestamp": log_data.get("timestamp", ""),
        "filename": log_data.get("filename", "unknown"),
        "start_time": start_time,
        "end_time": end_time,
        "message_count": metadata.get("message_count", 0),
        "tool_call_count": metadata.get("tool_call_count", 0),
        "num_tools": metadata.get("num_tools", 0),
        "iteration_count": workspace_state.get("iteration_count", 0),
        "errors": all_errors,
        "has_errors": len(all_errors) > 0,
        "llm_model": metadata.get("llm_model", "unknown"),
    }

    # Extract scratchpad data from workspace_state
    scratchpad = workspace_state.get("scratchpad", {})
    # The scratchpad contains "iterations" which are ontology refinement iterations (different from agent_iterations)
    ontology_iterations = scratchpad.get("iterations", [])

    metrics["iterations_data"] = (
        ontology_iterations if isinstance(ontology_iterations, list) else []
    )
    metrics["final_syntax_valid"] = False
    metrics["final_pitfalls"] = None
    metrics["pitfalls_list"] = []
    metrics["final_status"] = "unknown"

    if (
        ontology_iterations
        and isinstance(ontology_iterations, list)
        and len(ontology_iterations) > 0
    ):
        last_iter = ontology_iterations[-1]
        if isinstance(last_iter, dict):
            metrics["final_syntax_valid"] = last_iter.get("syntax_valid", False)
            metrics["final_pitfalls"] = last_iter.get("pitfalls_found", 0)
            metrics["final_status"] = last_iter.get("status", "unknown")

            # Collect all pitfalls encountered
            for iter_data in ontology_iterations:
                if isinstance(iter_data, dict):
                    pitfall_codes = iter_data.get("pitfall_codes", [])
                    if pitfall_codes and isinstance(pitfall_codes, list):
                        metrics["pitfalls_list"].extend(pitfall_codes)
                    # Also try to get from pitfall_details for backward compatibility
                    pitfall_details = iter_data.get("pitfall_details", "")
                    if (
                        pitfall_details
                        and isinstance(pitfall_details, str)
                        and "P" in pitfall_details
                    ):
                        metrics["pitfalls_list"].append(pitfall_details)

    # Check if final ontology was saved
    metrics["ontology_saved"] = bool(workspace_state.get("generated_owl"))

    # Calculate duration if available
    metrics["duration_seconds"] = calculate_duration_seconds(
        metrics["start_time"], metrics["end_time"]
    )

    # Extract tool usage from metadata
    tool_names = metadata.get("tool_names", [])
    metrics["tools_used"] = tool_names if isinstance(tool_names, list) else []

    # Count tool calls by type - aggregate from all agent iterations
    all_tool_calls = []
    for iter_data in agent_iterations:
        all_tool_calls.extend(iter_data.get("tool_calls", []))

    if all_tool_calls:
        tool_call_counts = Counter(
            [tc.get("name", "unknown") for tc in all_tool_calls if isinstance(tc, dict)]
        )
        metrics["tool_call_breakdown"] = dict(tool_call_counts)
    else:
        metrics["tool_call_breakdown"] = {}

    # Success determination for generator:
    # Generator success = agent completed task and saved ontology without execution errors
    # Syntax and pitfall validation are handled by the validation pipeline, not generator success
    metrics["success"] = metrics["ontology_saved"] and not metrics["has_errors"]

    return metrics


def extract_validation_metrics(log_data):
    """Extract key metrics from a single validation log file."""
    metrics = {
        "story_id": log_data.get("story_id", "unknown"),
        "timestamp": log_data.get("timestamp", ""),
        "filename": log_data.get("filename", "unknown"),
        "start_time": log_data.get("start_time", ""),
        "end_time": log_data.get("end_time", ""),
        "ontology_size_chars": log_data.get("ontology_size_chars", 0),
        "iteration_count": log_data.get("iteration_count", 0),
    }

    # Extract validation results
    validation_results = log_data.get("validation_results", {})

    # Syntax validation
    syntax = validation_results.get("syntax", {})
    metrics["syntax_valid"] = syntax.get("valid", False)
    metrics["syntax_time_seconds"] = syntax.get("execution_time_seconds", 0.0)
    metrics["syntax_error"] = syntax.get("error")

    # OOPS validation
    oops = validation_results.get("oops", {})
    metrics["oops_has_pitfalls"] = oops.get("has_pitfalls", False)
    metrics["oops_pitfall_count"] = oops.get("pitfall_count", 0)
    metrics["oops_time_seconds"] = oops.get("execution_time_seconds", 0.0)
    metrics["oops_pitfall_codes"] = oops.get("pitfall_codes", [])
    metrics["oops_pitfalls"] = oops.get("pitfalls", [])

    # Analyze pitfall severity
    pitfalls = oops.get("pitfalls", [])
    metrics["has_critical_pitfalls"] = False
    metrics["has_important_pitfalls"] = False
    metrics["has_only_minor_pitfalls"] = False
    metrics["critical_pitfall_count"] = 0
    metrics["important_pitfall_count"] = 0
    metrics["minor_pitfall_count"] = 0

    for p in pitfalls:
        importance = p.get("importance", "").lower()
        if importance == "critical":
            metrics["has_critical_pitfalls"] = True
            metrics["critical_pitfall_count"] += 1
        elif importance == "important":
            metrics["has_important_pitfalls"] = True
            metrics["important_pitfall_count"] += 1
        elif importance == "minor":
            metrics["minor_pitfall_count"] += 1

    # Determine if only minor pitfalls exist
    if (
        metrics["oops_has_pitfalls"]
        and not metrics["has_critical_pitfalls"]
        and not metrics["has_important_pitfalls"]
    ):
        metrics["has_only_minor_pitfalls"] = True

    # Hermit reasoner validation
    hermit = validation_results.get("hermit", {})
    metrics["hermit_consistent"] = hermit.get("is_consistent", False)
    metrics["hermit_time_seconds"] = hermit.get("execution_time_seconds", 0.0)
    metrics["hermit_inconsistent_classes"] = hermit.get("inconsistent_classes", [])
    metrics["hermit_inconsistent_count"] = hermit.get("inconsistent_classes_count", 0)
    metrics["hermit_error"] = hermit.get("error")
    metrics["hermit_error_type"] = hermit.get("error_type")

    # Pellet reasoner validation
    pellet = validation_results.get("pellet", {})
    metrics["pellet_consistent"] = pellet.get("is_consistent", False)
    metrics["pellet_time_seconds"] = pellet.get("execution_time_seconds", 0.0)
    metrics["pellet_inconsistent_classes"] = pellet.get("inconsistent_classes", [])
    metrics["pellet_inconsistent_count"] = pellet.get("inconsistent_classes_count", 0)
    metrics["pellet_error"] = pellet.get("error")
    metrics["pellet_error_type"] = pellet.get("error_type")

    # Aggregate results
    aggregate = validation_results.get("aggregate", {})
    metrics["all_validators_passed"] = aggregate.get("all_validators_passed", False)
    metrics["total_execution_time_seconds"] = aggregate.get(
        "total_execution_time_seconds", 0.0
    )

    # Calculate duration if available
    metrics["duration_seconds"] = calculate_duration_seconds(
        metrics["start_time"], metrics["end_time"]
    )

    return metrics


def analyze_all_logs(logs):
    """Perform comprehensive analysis on all generator logs."""
    all_metrics = [extract_metrics(log) for log in logs]

    # Group by story
    by_story = defaultdict(list)
    for m in all_metrics:
        by_story[m["story_id"]].append(m)

    analysis = {
        "total_runs": len(all_metrics),
        "by_story": {},
        "overall": {},
        "pitfalls_analysis": {},
        "tool_usage": {},
        "temporal_analysis": {},
    }

    # Overall statistics
    successes = sum(1 for m in all_metrics if m["success"])
    analysis["overall"]["success_rate"] = (
        successes / len(all_metrics) * 100 if all_metrics else 0
    )
    analysis["overall"]["total_successes"] = successes
    analysis["overall"]["total_failures"] = len(all_metrics) - successes

    # Iteration statistics
    iterations = [m["iteration_count"] for m in all_metrics if m["iteration_count"] > 0]
    if iterations:
        analysis["overall"]["avg_iterations"] = statistics.mean(iterations)
        analysis["overall"]["median_iterations"] = statistics.median(iterations)
        analysis["overall"]["max_iterations"] = max(iterations)
        analysis["overall"]["min_iterations"] = min(iterations)

    # Duration statistics
    durations = [m["duration_seconds"] for m in all_metrics if m["duration_seconds"]]
    if durations:
        analysis["overall"]["avg_duration_seconds"] = statistics.mean(durations)
        analysis["overall"]["median_duration_seconds"] = statistics.median(durations)
        analysis["overall"]["max_duration_seconds"] = max(durations)
        analysis["overall"]["min_duration_seconds"] = min(durations)

    # Message/tool call statistics
    msg_counts = [m["message_count"] for m in all_metrics if m["message_count"] > 0]
    tool_counts = [
        m["tool_call_count"] for m in all_metrics if m["tool_call_count"] > 0
    ]

    if msg_counts:
        analysis["overall"]["avg_messages"] = statistics.mean(msg_counts)
        analysis["overall"]["median_messages"] = statistics.median(msg_counts)

    if tool_counts:
        analysis["overall"]["avg_tool_calls"] = statistics.mean(tool_counts)
        analysis["overall"]["median_tool_calls"] = statistics.median(tool_counts)

    # Per-story analysis
    for story_id, story_metrics in by_story.items():
        story_analysis = {}
        story_successes = sum(1 for m in story_metrics if m["success"])
        story_analysis["run_count"] = len(story_metrics)
        story_analysis["success_rate"] = story_successes / len(story_metrics) * 100
        story_analysis["successes"] = story_successes
        story_analysis["failures"] = len(story_metrics) - story_successes

        # Story-specific iteration stats
        story_iters = [
            m["iteration_count"] for m in story_metrics if m["iteration_count"] > 0
        ]
        if story_iters:
            story_analysis["avg_iterations"] = statistics.mean(story_iters)
            story_analysis["median_iterations"] = statistics.median(story_iters)

        # Story-specific duration
        story_durations = [
            m["duration_seconds"] for m in story_metrics if m["duration_seconds"]
        ]
        if story_durations:
            story_analysis["avg_duration_seconds"] = statistics.mean(story_durations)

        analysis["by_story"][story_id] = story_analysis

    # Pitfalls analysis
    all_pitfalls = []
    for m in all_metrics:
        all_pitfalls.extend(m["pitfalls_list"])

    pitfall_counter = Counter()
    for pitfall_desc in all_pitfalls:
        # Extract pitfall code (e.g., P13)
        matches = re.findall(r"P\d+", pitfall_desc)
        for match in matches:
            pitfall_counter[match] += 1

    analysis["pitfalls_analysis"]["most_common"] = pitfall_counter.most_common()
    analysis["pitfalls_analysis"]["total_pitfall_occurrences"] = sum(
        pitfall_counter.values()
    )
    analysis["pitfalls_analysis"]["unique_pitfalls"] = len(pitfall_counter)

    # Tool usage analysis
    all_tool_calls = defaultdict(int)
    for m in all_metrics:
        for tool, count in m["tool_call_breakdown"].items():
            all_tool_calls[tool] += count

    analysis["tool_usage"]["total_calls"] = sum(all_tool_calls.values())
    analysis["tool_usage"]["by_tool"] = dict(
        sorted(all_tool_calls.items(), key=lambda x: x[1], reverse=True)
    )

    # Temporal analysis (runs over time)
    timestamped_metrics = [m for m in all_metrics if m["timestamp"]]
    timestamped_metrics.sort(key=lambda x: x["timestamp"])

    if len(timestamped_metrics) >= 10:
        # First 10 runs vs last 10 runs
        first_10 = timestamped_metrics[:10]
        last_10 = timestamped_metrics[-10:]

        first_10_success = sum(1 for m in first_10 if m["success"])
        last_10_success = sum(1 for m in last_10 if m["success"])

        analysis["temporal_analysis"]["first_10_success_rate"] = (
            first_10_success / 10 * 100
        )
        analysis["temporal_analysis"]["last_10_success_rate"] = (
            last_10_success / 10 * 100
        )
        analysis["temporal_analysis"]["improvement"] = (
            last_10_success / 10 * 100 - first_10_success / 10 * 100
        )

    return analysis, all_metrics


def analyze_validation_logs(validation_logs):
    """Perform comprehensive analysis on all validation logs."""
    all_metrics = [extract_validation_metrics(log) for log in validation_logs]

    if not all_metrics:
        return {}, []

    # Group by story
    by_story = defaultdict(list)
    for m in all_metrics:
        by_story[m["story_id"]].append(m)

    analysis = {
        "total_validations": len(all_metrics),
        "by_story": {},
        "overall": {},
        "reasoner_analysis": {},
        "oops_analysis": {},
        "timing_analysis": {},
    }

    # Overall statistics
    all_passed = sum(1 for m in all_metrics if m["all_validators_passed"])
    syntax_valid = sum(1 for m in all_metrics if m["syntax_valid"])
    hermit_consistent = sum(1 for m in all_metrics if m["hermit_consistent"])
    pellet_consistent = sum(1 for m in all_metrics if m["pellet_consistent"])
    oops_passed = sum(1 for m in all_metrics if not m["oops_has_pitfalls"])

    analysis["overall"]["all_passed_rate"] = (
        all_passed / len(all_metrics) * 100 if all_metrics else 0
    )
    analysis["overall"]["all_passed_count"] = all_passed
    analysis["overall"]["syntax_valid_count"] = syntax_valid
    analysis["overall"]["syntax_valid_rate"] = (
        syntax_valid / len(all_metrics) * 100 if all_metrics else 0
    )
    analysis["overall"]["oops_passed_count"] = oops_passed
    analysis["overall"]["oops_passed_rate"] = (
        oops_passed / len(all_metrics) * 100 if all_metrics else 0
    )

    # OOPS severity-based statistics
    # Count runs without Critical or Important pitfalls (ignoring Minor)
    oops_no_critical_important = sum(
        1
        for m in all_metrics
        if not m["has_critical_pitfalls"] and not m["has_important_pitfalls"]
    )
    # Count runs with only minor pitfalls
    oops_only_minor = sum(1 for m in all_metrics if m["has_only_minor_pitfalls"])

    analysis["overall"]["oops_no_critical_important_count"] = oops_no_critical_important
    analysis["overall"]["oops_no_critical_important_rate"] = (
        oops_no_critical_important / len(all_metrics) * 100 if all_metrics else 0
    )
    analysis["overall"]["oops_only_minor_count"] = oops_only_minor
    analysis["overall"]["oops_only_minor_rate"] = (
        oops_only_minor / len(all_metrics) * 100 if all_metrics else 0
    )

    # Reasoner analysis
    analysis["reasoner_analysis"]["hermit_consistent_count"] = hermit_consistent
    analysis["reasoner_analysis"]["hermit_consistent_rate"] = (
        hermit_consistent / len(all_metrics) * 100 if all_metrics else 0
    )
    analysis["reasoner_analysis"]["pellet_consistent_count"] = pellet_consistent
    analysis["reasoner_analysis"]["pellet_consistent_rate"] = (
        pellet_consistent / len(all_metrics) * 100 if all_metrics else 0
    )

    # Both reasoners consistent
    both_consistent = sum(
        1 for m in all_metrics if m["hermit_consistent"] and m["pellet_consistent"]
    )
    analysis["reasoner_analysis"]["both_consistent_count"] = both_consistent
    analysis["reasoner_analysis"]["both_consistent_rate"] = (
        both_consistent / len(all_metrics) * 100 if all_metrics else 0
    )

    # Reasoner errors
    hermit_errors = sum(1 for m in all_metrics if m["hermit_error"])
    pellet_errors = sum(1 for m in all_metrics if m["pellet_error"])
    analysis["reasoner_analysis"]["hermit_error_count"] = hermit_errors
    analysis["reasoner_analysis"]["pellet_error_count"] = pellet_errors

    # Collect unique error messages with counts
    hermit_error_messages = Counter()
    pellet_error_messages = Counter()
    for m in all_metrics:
        if m["hermit_error"]:
            # Extract the main error message (first meaningful line)
            error_msg = m["hermit_error"]
            # Try to extract the key part of the error
            if "IllegalArgumentException:" in error_msg:
                # Extract the exception message
                parts = error_msg.split("IllegalArgumentException:")
                if len(parts) > 1:
                    key_msg = (
                        "IllegalArgumentException:" + parts[1].split("\n")[0].strip()
                    )
                else:
                    key_msg = error_msg.split("\n")[0][:200]
            elif "Exception" in error_msg:
                key_msg = error_msg.split("\n")[0][:200]
            else:
                key_msg = error_msg[:200]
            hermit_error_messages[key_msg] += 1
        if m["pellet_error"]:
            error_msg = m["pellet_error"]
            if "IllegalArgumentException:" in error_msg:
                parts = error_msg.split("IllegalArgumentException:")
                if len(parts) > 1:
                    key_msg = (
                        "IllegalArgumentException:" + parts[1].split("\n")[0].strip()
                    )
                else:
                    key_msg = error_msg.split("\n")[0][:200]
            elif "Exception" in error_msg:
                key_msg = error_msg.split("\n")[0][:200]
            else:
                key_msg = error_msg[:200]
            pellet_error_messages[key_msg] += 1

    analysis["reasoner_analysis"]["hermit_error_messages"] = dict(
        hermit_error_messages.most_common()
    )
    analysis["reasoner_analysis"]["pellet_error_messages"] = dict(
        pellet_error_messages.most_common()
    )

    # Collect inconsistent classes
    all_hermit_inconsistent = []
    all_pellet_inconsistent = []
    for m in all_metrics:
        all_hermit_inconsistent.extend(m["hermit_inconsistent_classes"])
        all_pellet_inconsistent.extend(m["pellet_inconsistent_classes"])

    analysis["reasoner_analysis"]["hermit_inconsistent_classes"] = list(
        set(all_hermit_inconsistent)
    )
    analysis["reasoner_analysis"]["pellet_inconsistent_classes"] = list(
        set(all_pellet_inconsistent)
    )

    # OOPS analysis
    all_pitfall_codes = []
    all_pitfalls_detailed = []
    for m in all_metrics:
        all_pitfall_codes.extend(m["oops_pitfall_codes"])
        all_pitfalls_detailed.extend(m["oops_pitfalls"])

    pitfall_counter = Counter(all_pitfall_codes)
    analysis["oops_analysis"]["most_common_pitfalls"] = pitfall_counter.most_common()
    analysis["oops_analysis"]["total_pitfall_occurrences"] = sum(
        pitfall_counter.values()
    )
    analysis["oops_analysis"]["unique_pitfalls"] = len(pitfall_counter)

    # Pitfall details
    pitfall_details = {}
    for p in all_pitfalls_detailed:
        code = p.get("code", "unknown")
        if code not in pitfall_details:
            pitfall_details[code] = {
                "name": p.get("name", ""),
                "description": p.get("description", ""),
                "importance": p.get("importance", ""),
                "occurrences": 0,
                "affected_elements": [],
            }
        pitfall_details[code]["occurrences"] += 1
        pitfall_details[code]["affected_elements"].extend(
            p.get("affected_elements", [])
        )

    analysis["oops_analysis"]["pitfall_details"] = pitfall_details

    # Timing analysis
    hermit_times = [
        m["hermit_time_seconds"] for m in all_metrics if m["hermit_time_seconds"] > 0
    ]
    pellet_times = [
        m["pellet_time_seconds"] for m in all_metrics if m["pellet_time_seconds"] > 0
    ]
    syntax_times = [
        m["syntax_time_seconds"] for m in all_metrics if m["syntax_time_seconds"] > 0
    ]
    oops_times = [
        m["oops_time_seconds"] for m in all_metrics if m["oops_time_seconds"] > 0
    ]
    total_times = [
        m["total_execution_time_seconds"]
        for m in all_metrics
        if m["total_execution_time_seconds"] > 0
    ]

    if hermit_times:
        analysis["timing_analysis"]["hermit_avg_seconds"] = statistics.mean(
            hermit_times
        )
        analysis["timing_analysis"]["hermit_median_seconds"] = statistics.median(
            hermit_times
        )

    if pellet_times:
        analysis["timing_analysis"]["pellet_avg_seconds"] = statistics.mean(
            pellet_times
        )
        analysis["timing_analysis"]["pellet_median_seconds"] = statistics.median(
            pellet_times
        )

    if syntax_times:
        analysis["timing_analysis"]["syntax_avg_seconds"] = statistics.mean(
            syntax_times
        )

    if oops_times:
        analysis["timing_analysis"]["oops_avg_seconds"] = statistics.mean(oops_times)

    if total_times:
        analysis["timing_analysis"]["total_avg_seconds"] = statistics.mean(total_times)
        analysis["timing_analysis"]["total_median_seconds"] = statistics.median(
            total_times
        )

    # Per-story analysis
    for story_id, story_metrics in by_story.items():
        story_analysis = {}
        story_analysis["validation_count"] = len(story_metrics)

        story_passed = sum(1 for m in story_metrics if m["all_validators_passed"])
        story_analysis["all_passed_rate"] = (
            story_passed / len(story_metrics) * 100 if story_metrics else 0
        )

        story_hermit = sum(1 for m in story_metrics if m["hermit_consistent"])
        story_pellet = sum(1 for m in story_metrics if m["pellet_consistent"])
        story_analysis["hermit_consistent_rate"] = (
            story_hermit / len(story_metrics) * 100 if story_metrics else 0
        )
        story_analysis["pellet_consistent_rate"] = (
            story_pellet / len(story_metrics) * 100 if story_metrics else 0
        )

        story_oops_passed = sum(1 for m in story_metrics if not m["oops_has_pitfalls"])
        story_analysis["oops_passed_rate"] = (
            story_oops_passed / len(story_metrics) * 100 if story_metrics else 0
        )

        analysis["by_story"][story_id] = story_analysis

    return analysis, all_metrics


def generate_report(
    analysis, all_metrics, validation_analysis=None, validation_metrics=None
):
    """Generate a comprehensive text report."""
    report = []
    report.append("=" * 80)
    report.append("OTHO AGENT LOG ANALYSIS - COMPREHENSIVE REPORT")
    report.append("=" * 80)
    report.append("")

    # Overall summary
    report.append("OVERALL SUMMARY (Generator Runs)")
    report.append("-" * 80)
    report.append(f"Total Runs Analyzed: {analysis['total_runs']}")
    report.append(f"Total Successes: {analysis['overall']['total_successes']}")
    report.append(f"Total Failures: {analysis['overall']['total_failures']}")
    report.append(f"Overall Success Rate: {analysis['overall']['success_rate']:.2f}%")
    report.append("")

    # Iteration statistics
    if "avg_iterations" in analysis["overall"]:
        report.append("ITERATION STATISTICS")
        report.append("-" * 80)
        report.append(
            f"Average Iterations: {analysis['overall']['avg_iterations']:.2f}"
        )
        report.append(
            f"Median Iterations: {analysis['overall']['median_iterations']:.1f}"
        )
        report.append(f"Min Iterations: {analysis['overall']['min_iterations']}")
        report.append(f"Max Iterations: {analysis['overall']['max_iterations']}")
        report.append("")

    # Duration statistics
    if "avg_duration_seconds" in analysis["overall"]:
        report.append("DURATION STATISTICS")
        report.append("-" * 80)
        report.append(
            f"Average Duration: {analysis['overall']['avg_duration_seconds']:.2f} seconds ({analysis['overall']['avg_duration_seconds'] / 60:.2f} minutes)"
        )
        report.append(
            f"Median Duration: {analysis['overall']['median_duration_seconds']:.2f} seconds"
        )
        report.append(
            f"Min Duration: {analysis['overall']['min_duration_seconds']:.2f} seconds"
        )
        report.append(
            f"Max Duration: {analysis['overall']['max_duration_seconds']:.2f} seconds"
        )
        report.append("")

    # Message/Tool call statistics
    if "avg_messages" in analysis["overall"]:
        report.append("COMMUNICATION STATISTICS")
        report.append("-" * 80)
        report.append(
            f"Average Messages per Run: {analysis['overall']['avg_messages']:.2f}"
        )
        report.append(
            f"Median Messages per Run: {analysis['overall']['median_messages']:.1f}"
        )
        report.append(
            f"Average Tool Calls per Run: {analysis['overall']['avg_tool_calls']:.2f}"
        )
        report.append(
            f"Median Tool Calls per Run: {analysis['overall']['median_tool_calls']:.1f}"
        )
        report.append("")

    # Per-story analysis
    report.append("PER-STORY ANALYSIS (Generator)")
    report.append("-" * 80)
    for story_id, story_data in sorted(analysis["by_story"].items()):
        report.append(f"\n{story_id}:")
        report.append(f"  Runs: {story_data['run_count']}")
        report.append(f"  Success Rate: {story_data['success_rate']:.2f}%")
        report.append(f"  Successes: {story_data['successes']}")
        report.append(f"  Failures: {story_data['failures']}")
        if "avg_iterations" in story_data:
            report.append(f"  Avg Iterations: {story_data['avg_iterations']:.2f}")
            report.append(f"  Median Iterations: {story_data['median_iterations']:.1f}")
        if "avg_duration_seconds" in story_data:
            report.append(
                f"  Avg Duration: {story_data['avg_duration_seconds']:.2f} seconds ({story_data['avg_duration_seconds'] / 60:.2f} minutes)"
            )
    report.append("")

    # Pitfalls analysis
    report.append("PITFALLS ANALYSIS (Generator)")
    report.append("-" * 80)
    report.append(
        f"Total Pitfall Occurrences: {analysis['pitfalls_analysis']['total_pitfall_occurrences']}"
    )
    report.append(
        f"Unique Pitfalls Encountered: {analysis['pitfalls_analysis']['unique_pitfalls']}"
    )
    report.append("\nMost Common Pitfalls:")
    for pitfall, count in analysis["pitfalls_analysis"]["most_common"][:10]:
        report.append(f"  {pitfall}: {count} occurrences")
    report.append("")

    # Tool usage
    report.append("TOOL USAGE ANALYSIS")
    report.append("-" * 80)
    report.append(f"Total Tool Calls: {analysis['tool_usage']['total_calls']}")
    report.append("\nTool Call Breakdown:")
    for tool, count in list(analysis["tool_usage"]["by_tool"].items())[:15]:
        percentage = count / analysis["tool_usage"]["total_calls"] * 100
        report.append(f"  {tool}: {count} calls ({percentage:.1f}%)")
    report.append("")

    # Temporal analysis
    if analysis["temporal_analysis"]:
        report.append("TEMPORAL ANALYSIS (Learning Over Time)")
        report.append("-" * 80)
        report.append(
            f"First 10 Runs Success Rate: {analysis['temporal_analysis']['first_10_success_rate']:.2f}%"
        )
        report.append(
            f"Last 10 Runs Success Rate: {analysis['temporal_analysis']['last_10_success_rate']:.2f}%"
        )
        report.append(
            f"Improvement: {analysis['temporal_analysis']['improvement']:+.2f} percentage points"
        )
        report.append("")

    # Failure analysis
    failures = [m for m in all_metrics if not m["success"]]
    if failures:
        report.append("FAILURE ANALYSIS (Generator)")
        report.append("-" * 80)
        report.append(f"Total Failures: {len(failures)}")
        report.append("\nFailure Reasons:")

        reasons = defaultdict(int)
        for m in failures:
            if m["has_errors"]:
                reasons["Execution Errors"] += 1
            if not m["ontology_saved"]:
                reasons["Ontology Not Saved"] += 1

        for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {reason}: {count}")
        report.append("")

    # Success patterns
    successes = [m for m in all_metrics if m["success"]]
    if successes:
        report.append("SUCCESS PATTERNS")
        report.append("-" * 80)
        success_iters = [
            m["iteration_count"] for m in successes if m["iteration_count"] > 0
        ]
        if success_iters:
            report.append(
                f"Average Iterations for Success: {statistics.mean(success_iters):.2f}"
            )
            report.append(
                f"Most Common Iteration Count: {Counter(success_iters).most_common(1)[0][0]}"
            )
        report.append("")

    # ========================================
    # VALIDATION ANALYSIS SECTION
    # ========================================
    if validation_analysis and validation_metrics:
        report.append("=" * 80)
        report.append("VALIDATION ANALYSIS (Reasoner Results)")
        report.append("=" * 80)
        report.append("")

        report.append("OVERALL VALIDATION SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Validations: {validation_analysis['total_validations']}")
        report.append(
            f"All Validators Passed: {validation_analysis['overall']['all_passed_count']} ({validation_analysis['overall']['all_passed_rate']:.2f}%)"
        )
        report.append(
            f"Syntax Valid: {validation_analysis['overall']['syntax_valid_count']} ({validation_analysis['overall']['syntax_valid_rate']:.2f}%)"
        )
        report.append(
            f"OOPS Passed (No Pitfalls): {validation_analysis['overall']['oops_passed_count']} ({validation_analysis['overall']['oops_passed_rate']:.2f}%)"
        )
        report.append(
            f"OOPS Passed (No Critical/Important): {validation_analysis['overall']['oops_no_critical_important_count']} ({validation_analysis['overall']['oops_no_critical_important_rate']:.2f}%)"
        )
        reasoner = validation_analysis["reasoner_analysis"]
        report.append(
            f"Reasoners Passed (Both Consistent): {reasoner['both_consistent_count']} ({reasoner['both_consistent_rate']:.2f}%)"
        )
        report.append("")

        # Reasoner Results
        report.append("REASONER VALIDATION RESULTS")
        report.append("-" * 80)
        reasoner = validation_analysis["reasoner_analysis"]
        report.append(
            f"Hermit Consistent: {reasoner['hermit_consistent_count']} ({reasoner['hermit_consistent_rate']:.2f}%)"
        )
        report.append(
            f"Pellet Consistent: {reasoner['pellet_consistent_count']} ({reasoner['pellet_consistent_rate']:.2f}%)"
        )
        report.append(
            f"Both Reasoners Consistent: {reasoner['both_consistent_count']} ({reasoner['both_consistent_rate']:.2f}%)"
        )
        report.append(f"Hermit Errors: {reasoner['hermit_error_count']}")
        report.append(f"Pellet Errors: {reasoner['pellet_error_count']}")

        # Display error reasons for Hermit
        if reasoner.get("hermit_error_messages"):
            report.append("\nHermit Error Reasons:")
            for error_msg, count in reasoner["hermit_error_messages"].items():
                report.append(f"  {count}x - {error_msg}")

        # Display error reasons for Pellet
        if reasoner.get("pellet_error_messages"):
            report.append("\nPellet Error Reasons:")
            for error_msg, count in reasoner["pellet_error_messages"].items():
                report.append(f"  {count}x - {error_msg}")

        if reasoner["hermit_inconsistent_classes"]:
            report.append("\nHermit Inconsistent Classes:")
            for cls in reasoner["hermit_inconsistent_classes"][:10]:
                report.append(f"  - {cls}")

        if reasoner["pellet_inconsistent_classes"]:
            report.append("\nPellet Inconsistent Classes:")
            for cls in reasoner["pellet_inconsistent_classes"][:10]:
                report.append(f"  - {cls}")
        report.append("")

        # OOPS Pitfalls from Validation
        report.append("OOPS PITFALLS (Validation)")
        report.append("-" * 80)
        oops = validation_analysis["oops_analysis"]
        overall = validation_analysis["overall"]
        report.append(f"Total Pitfall Occurrences: {oops['total_pitfall_occurrences']}")
        report.append(f"Unique Pitfalls: {oops['unique_pitfalls']}")
        report.append("")
        report.append("Severity Breakdown:")
        report.append(
            f"  Runs Passed (No Pitfalls): {overall['oops_passed_count']} ({overall['oops_passed_rate']:.2f}%)"
        )
        report.append(
            f"  Runs Passed (No Critical/Important): {overall['oops_no_critical_important_count']} ({overall['oops_no_critical_important_rate']:.2f}%)"
        )
        report.append(
            f"  Runs with Only Minor Pitfalls: {overall['oops_only_minor_count']} ({overall['oops_only_minor_rate']:.2f}%)"
        )
        report.append("\nMost Common Pitfalls:")
        for pitfall, count in oops["most_common_pitfalls"][:10]:
            # Get pitfall name if available
            details = oops["pitfall_details"].get(pitfall, {})
            name = details.get("name", "")
            importance = details.get("importance", "")
            if name:
                report.append(f"  {pitfall} ({importance}): {count} - {name}")
            else:
                report.append(f"  {pitfall}: {count}")
        report.append("")

        # Timing Analysis
        if validation_analysis["timing_analysis"]:
            report.append("VALIDATION TIMING ANALYSIS")
            report.append("-" * 80)
            timing = validation_analysis["timing_analysis"]
            if "hermit_avg_seconds" in timing:
                report.append(
                    f"Hermit Avg Time: {timing['hermit_avg_seconds']:.3f}s (median: {timing['hermit_median_seconds']:.3f}s)"
                )
            if "pellet_avg_seconds" in timing:
                report.append(
                    f"Pellet Avg Time: {timing['pellet_avg_seconds']:.3f}s (median: {timing['pellet_median_seconds']:.3f}s)"
                )
            if "syntax_avg_seconds" in timing:
                report.append(f"Syntax Avg Time: {timing['syntax_avg_seconds']:.3f}s")
            if "oops_avg_seconds" in timing:
                report.append(f"OOPS Avg Time: {timing['oops_avg_seconds']:.3f}s")
            if "total_avg_seconds" in timing:
                report.append(
                    f"Total Validation Avg Time: {timing['total_avg_seconds']:.3f}s"
                )
            report.append("")

        # Per-story Validation Analysis
        report.append("PER-STORY VALIDATION ANALYSIS")
        report.append("-" * 80)
        for story_id, story_data in sorted(validation_analysis["by_story"].items()):
            report.append(f"\n{story_id}:")
            report.append(f"  Validations: {story_data['validation_count']}")
            report.append(f"  All Passed Rate: {story_data['all_passed_rate']:.2f}%")
            report.append(
                f"  Hermit Consistent Rate: {story_data['hermit_consistent_rate']:.2f}%"
            )
            report.append(
                f"  Pellet Consistent Rate: {story_data['pellet_consistent_rate']:.2f}%"
            )
            report.append(f"  OOPS Passed Rate: {story_data['oops_passed_rate']:.2f}%")
        report.append("")

        # Per-run Validation Results Table
        report.append("PER-RUN VALIDATION RESULTS")
        report.append("-" * 80)
        # Table header
        report.append(
            f"{'Timestamp':<20} | {'Syntax':^8} | {'OOPS':^8} | {'Hermit':^8} | {'Pellet':^8}"
        )
        report.append("-" * 62)
        # Sort by timestamp and add each row
        sorted_metrics = sorted(validation_metrics, key=lambda x: x["timestamp"])
        for m in sorted_metrics:
            timestamp = m["timestamp"]
            syntax = "  ✓" if m["syntax_valid"] else "  x"
            oops = "  ✓" if not m["oops_has_pitfalls"] else "  x"
            hermit = "  ✓" if m["hermit_consistent"] else "  x"
            pellet = "  ✓" if m["pellet_consistent"] else "  x"
            report.append(
                f"{timestamp:<20} | {syntax:^8} | {oops:^8} | {hermit:^8} | {pellet:^8}"
            )
        report.append("")
        report.append("Legend: ✓ = passed, x = failed")
        report.append("")

    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    """Main execution function."""
    print("Loading generator log files...")
    logs = load_all_logs()
    print(f"Loaded {len(logs)} generator log files")

    print("\nLoading validation log files...")
    validation_logs = load_validation_logs()
    print(f"Loaded {len(validation_logs)} validation log files")

    print("\nAnalyzing generator logs...")
    analysis, all_metrics = analyze_all_logs(logs)

    print("\nAnalyzing validation logs...")
    validation_analysis, validation_metrics = analyze_validation_logs(validation_logs)

    print("\nGenerating report...")
    report = generate_report(
        analysis, all_metrics, validation_analysis, validation_metrics
    )

    # Print to console
    print("\n" + report)

    # Save to file
    output_file = "log_analysis_report.txt"
    with open(output_file, "w") as f:
        f.write(report)
    print(f"\n\nReport saved to: {output_file}")

    # Also save raw analysis data as JSON
    analysis_file = "log_analysis_data.json"
    # Convert to JSON-serializable format
    json_data = {
        "generator_analysis": {
            "total_runs": analysis["total_runs"],
            "overall": analysis["overall"],
            "by_story": analysis["by_story"],
            "pitfalls_analysis": analysis["pitfalls_analysis"],
            "tool_usage": analysis["tool_usage"],
            "temporal_analysis": analysis["temporal_analysis"],
        },
        "validation_analysis": {
            "total_validations": validation_analysis.get("total_validations", 0),
            "overall": validation_analysis.get("overall", {}),
            "by_story": validation_analysis.get("by_story", {}),
            "reasoner_analysis": validation_analysis.get("reasoner_analysis", {}),
            "oops_analysis": {
                "most_common_pitfalls": validation_analysis.get(
                    "oops_analysis", {}
                ).get("most_common_pitfalls", []),
                "total_pitfall_occurrences": validation_analysis.get(
                    "oops_analysis", {}
                ).get("total_pitfall_occurrences", 0),
                "unique_pitfalls": validation_analysis.get("oops_analysis", {}).get(
                    "unique_pitfalls", 0
                ),
            },
            "timing_analysis": validation_analysis.get("timing_analysis", {}),
        },
    }

    with open(analysis_file, "w") as f:
        json.dump(json_data, f, indent=2)
    print(f"Raw analysis data saved to: {analysis_file}")


if __name__ == "__main__":
    main()
