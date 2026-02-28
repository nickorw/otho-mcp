"""
Comprehensive logging for validation results.

Provides detailed logging of all validation steps including syntax checks,
pitfall detection, and reasoner consistency checks with complete failure details.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utils.timing import format_duration


class ValidationLogger:
    """
    Logger for validation execution with support for multiple output formats.

    Logs to:
    - Console (INFO level)
    - File log (DEBUG level with detailed formatting)
    - JSON structured log (complete validation results with full details)
    """

    def __init__(
        self, story_id: str, log_dir: str = "logs", timestamp: Optional[str] = None
    ):
        """
        Initialize validation logger.

        Args:
            story_id: Story identifier for log file naming
            log_dir: Directory for log files (default: logs/)
            timestamp: Pre-defined timestamp for log file naming (shared with generator logs).
                       If None, a new timestamp is generated.
        """
        self.story_id = story_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Use provided timestamp or create new one
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

        # Set up file logger with validation in filename
        self.text_log_path = (
            self.log_dir / f"{story_id}_validation_{self.timestamp}.log"
        )
        self.json_log_path = (
            self.log_dir / f"{story_id}_validation_{self.timestamp}.json"
        )

        # Configure Python logger - include timestamp in logger name to avoid conflicts
        self.logger = logging.getLogger(f"validation.{story_id}.{self.timestamp}")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # File handler - detailed DEBUG logs
        file_handler = logging.FileHandler(
            self.text_log_path, mode="w", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler - INFO and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Structured data for JSON log
        self.json_data = {
            "story_id": story_id,
            "timestamp": self.timestamp,
            "start_time": datetime.now().isoformat(),
            "ontology_size_chars": 0,
            "validation_results": {},
            "files_saved": [],
        }

        self.logger.info(f"{'=' * 60}")
        self.logger.info(f"Validation Logger Initialized for {story_id}")
        self.logger.info(f"Log files: {self.text_log_path.name}")
        self.logger.info(f"Timestamp: {self.timestamp}")
        self.logger.info(f"{'=' * 60}")

    def log_start(self, ontology_size: int):
        """Log validation start."""
        self.logger.info(f"\nStarting final validation for {self.story_id}")
        self.logger.debug(f"Ontology size: {ontology_size} characters")
        self.json_data["ontology_size_chars"] = ontology_size

    def log_syntax_validation(
        self, is_valid: bool, execution_time_seconds: float, error: Optional[str] = None
    ):
        """Log syntax validation results with full error details."""
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("PILLAR 1: SYNTAX VALIDATION (RDFLib)")
        self.logger.info(f"{'=' * 60}")

        if is_valid:
            self.logger.info(
                f"✓ Syntax validation PASSED ({execution_time_seconds:.3f}s)"
            )
            self.logger.debug("No syntax errors detected in RDF/Turtle parsing")
        else:
            self.logger.error(
                f"✗ Syntax validation FAILED ({execution_time_seconds:.3f}s)"
            )
            self.logger.error(f"\nSyntax Error Details:")
            if error:
                # Log full error with line breaks preserved
                error_lines = error.split("\n")
                for line in error_lines:
                    self.logger.error(f"  {line}")
            else:
                self.logger.error("  No error message available")

        self.json_data["validation_results"]["syntax"] = {
            "valid": is_valid,
            "execution_time_seconds": round(execution_time_seconds, 3),
            "error": error,
            "error_type": "RDF/Turtle parsing error" if not is_valid else None,
        }

    def log_pitfall_detection(
        self,
        has_pitfalls: bool,
        pitfall_count: int,
        execution_time_seconds: float,
        pitfalls: List[Dict[str, Any]],
    ):
        """Log OOPS pitfall detection results with complete pitfall details."""
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("PILLAR 2: PITFALL DETECTION (OOPS)")
        self.logger.info(f"{'=' * 60}")

        if not has_pitfalls:
            self.logger.info(
                f"✓ Pitfall check PASSED - No pitfalls detected ({execution_time_seconds:.3f}s)"
            )
            self.logger.debug("All checked OOPS pitfall categories passed successfully")
        else:
            self.logger.warning(
                f"⚠ Pitfall check: Found {pitfall_count} pitfall(s) ({execution_time_seconds:.3f}s)"
            )
            pitfall_codes = [p.get("code", "") for p in pitfalls]
            self.logger.warning(f"Pitfall codes detected: {', '.join(pitfall_codes)}")

            # Log detailed information for each pitfall
            self.logger.warning(f"\nDetailed Pitfall Information:")
            self.logger.warning(f"{'-' * 60}")

            for idx, pitfall in enumerate(pitfalls, 1):
                code = pitfall.get("code", "Unknown")
                name = pitfall.get("name", "N/A")
                description = pitfall.get("description", "N/A")
                importance = pitfall.get("importance", "N/A")
                affected = pitfall.get("affected_elements", [])

                self.logger.warning(f"\nPitfall #{idx}: {code}")
                self.logger.warning(f"  Name: {name}")
                self.logger.warning(f"  Importance: {importance}")
                self.logger.warning(f"  Description: {description}")

                if affected:
                    self.logger.warning(f"  Affected Elements ({len(affected)} total):")
                    # Log first 10 affected elements to avoid log spam
                    for elem in affected[:10]:
                        self.logger.warning(f"    - {elem}")
                    if len(affected) > 10:
                        self.logger.warning(
                            f"    ... and {len(affected) - 10} more elements"
                        )
                else:
                    self.logger.warning(f"  Affected Elements: None specified")

                # Log detailed explanation if available
                if pitfall.get("explanation"):
                    self.logger.debug(f"  Explanation: {pitfall.get('explanation')}")

        # Store complete pitfall data in JSON
        self.json_data["validation_results"]["oops"] = {
            "has_pitfalls": has_pitfalls,
            "pitfall_count": pitfall_count,
            "execution_time_seconds": round(execution_time_seconds, 3),
            "pitfalls": pitfalls,  # Complete pitfall objects with all details
            "pitfall_codes": [p.get("code") for p in pitfalls],
            "pitfall_names": [p.get("name") for p in pitfalls],
        }

    def log_reasoner_validation(self, reasoner_name: str, result: Dict[str, Any]):
        """Log reasoner validation results with complete inconsistency details."""
        self.logger.info(f"\n  → {reasoner_name} Reasoner")
        self.logger.info(f"  {'-' * 56}")

        is_consistent = result.get("is_consistent", False)
        execution_time_seconds = result.get("execution_time_seconds", 0.0)
        error = result.get("error")
        inconsistent_classes = result.get("inconsistent_classes", [])

        if is_consistent:
            self.logger.info(
                f"  ✓ PASSED - Ontology is logically consistent ({execution_time_seconds:.3f}s)"
            )
            self.logger.debug(
                f"  {reasoner_name} found no logical inconsistencies or contradictions"
            )
        else:
            self.logger.error(
                f"  ✗ FAILED - Inconsistencies detected ({execution_time_seconds:.3f}s)"
            )

            if error:
                self.logger.error(f"\n  Error Details:")
                error_lines = str(error).split("\n")
                for line in error_lines:
                    self.logger.error(f"    {line}")

            if inconsistent_classes:
                self.logger.error(
                    f"\n  Inconsistent Classes ({len(inconsistent_classes)} found):"
                )
                for cls in inconsistent_classes:
                    self.logger.error(f"    - {cls}")
                self.logger.error(
                    f"\n  These classes contain logical contradictions that make them unsatisfiable."
                )
            elif not error:
                self.logger.error(
                    f"  Reasoner reported inconsistency but provided no specific details."
                )

        # Store complete reasoner data in JSON
        self.json_data["validation_results"][reasoner_name.lower()] = {
            "reasoner": reasoner_name,
            "is_consistent": is_consistent,
            "execution_time_seconds": round(execution_time_seconds, 3),
            "inconsistent_classes": inconsistent_classes,
            "inconsistent_classes_count": len(inconsistent_classes),
            "error": error,
            "error_type": "reasoning_error" if error else None,
        }

    def log_reasoning_start(self):
        """Log start of reasoning consistency checks."""
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("PILLAR 3: REASONING CONSISTENCY")
        self.logger.info(f"{'=' * 60}")
        self.logger.debug(
            "Checking logical consistency with OWL 2 DL reasoners (Hermit & Pellet)"
        )

    def log_file_saved(self, file_path: str, description: str):
        """Log saved file."""
        self.logger.info(f"✓ {description}: {file_path}")
        self.json_data["files_saved"].append(
            {
                "path": file_path,
                "description": description,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def log_story_complete(self, duration_seconds: float):
        """
        Log story completion with total duration.

        Args:
            duration_seconds: Total story duration in seconds
        """
        duration_formatted = format_duration(duration_seconds)

        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("STORY COMPLETION")
        self.logger.info(f"{'=' * 60}")
        self.logger.info(
            f"Total story duration: {duration_seconds:.2f}s ({duration_formatted})"
        )

        # Store in JSON data
        self.json_data["story_timing"] = {
            "duration_seconds": round(duration_seconds, 2),
            "duration_formatted": duration_formatted,
        }

    def log_summary(
        self,
        syntax_valid: bool,
        has_pitfalls: bool,
        pitfall_count: int,
        hermit_consistent: bool,
        pellet_consistent: bool,
        syntax_time_seconds: float,
        oops_time_seconds: float,
        hermit_time_seconds: float,
        pellet_time_seconds: float,
        iteration_count: int,
    ):
        """Log final validation summary with complete status breakdown."""
        total_time_seconds = (
            syntax_time_seconds
            + oops_time_seconds
            + hermit_time_seconds
            + pellet_time_seconds
        )
        all_passed = (
            syntax_valid
            and not has_pitfalls
            and hermit_consistent
            and pellet_consistent
        )

        self.logger.info(f"\n{'=' * 60}")
        self.logger.info("VALIDATION SUMMARY")
        self.logger.info(f"{'=' * 60}")

        # Detailed status for each validation pillar
        self.logger.info(
            f"1. Syntax (RDFLib):    {'✓ PASSED' if syntax_valid else '✗ FAILED'} ({syntax_time_seconds:.3f}s)"
        )
        if not syntax_valid:
            self.logger.error(
                f"   └─ RDF/Turtle parsing failed - check syntax error details above"
            )

        self.logger.info(
            f"2. OOPS Pitfalls:      {'✓ PASSED' if not has_pitfalls else f'⚠ FAILED ({pitfall_count} pitfalls)'} ({oops_time_seconds:.3f}s)"
        )
        if has_pitfalls:
            self.logger.warning(
                f"   └─ {pitfall_count} modeling pitfall(s) detected - check details above"
            )

        self.logger.info(
            f"3. Hermit Reasoner:    {'✓ PASSED' if hermit_consistent else '✗ FAILED'} ({hermit_time_seconds:.3f}s)"
        )
        if not hermit_consistent:
            self.logger.error(
                f"   └─ Logical inconsistencies found - check inconsistent classes above"
            )

        self.logger.info(
            f"4. Pellet Reasoner:    {'✓ PASSED' if pellet_consistent else '✗ FAILED'} ({pellet_time_seconds:.3f}s)"
        )
        if not pellet_consistent:
            self.logger.error(
                f"   └─ Logical inconsistencies found - check inconsistent classes above"
            )

        self.logger.info(f"{'-' * 60}")
        if all_passed:
            self.logger.info(f"Overall Result:        ✅ ALL VALIDATORS PASSED")
            self.logger.info(
                f"                       Ontology is syntactically valid, free of pitfalls,"
            )
            self.logger.info(f"                       and logically consistent.")
        else:
            self.logger.error(f"Overall Result:        ❌ VALIDATION FAILED")
            failures = []
            if not syntax_valid:
                failures.append("syntax errors")
            if has_pitfalls:
                failures.append(f"{pitfall_count} pitfalls")
            if not hermit_consistent:
                failures.append("Hermit inconsistencies")
            if not pellet_consistent:
                failures.append("Pellet inconsistencies")
            self.logger.error(
                f"                       Issues found: {', '.join(failures)}"
            )

        self.logger.info(f"{'-' * 60}")
        self.logger.info(f"Total Validation Time: {total_time_seconds:.3f}s")
        self.logger.info(f"Agent Iterations:      {iteration_count}")
        self.logger.info(f"{'=' * 60}")

        # Store aggregate results with detailed breakdown
        self.json_data["validation_results"]["aggregate"] = {
            "all_validators_passed": all_passed,
            "total_execution_time_seconds": round(total_time_seconds, 3),
            "validation_breakdown": {
                "syntax_valid": syntax_valid,
                "oops_passed": not has_pitfalls,
                "oops_pitfall_count": pitfall_count,
                "hermit_consistent": hermit_consistent,
                "pellet_consistent": pellet_consistent,
            },
            "timing_breakdown_seconds": {
                "syntax": round(syntax_time_seconds, 3),
                "oops": round(oops_time_seconds, 3),
                "hermit": round(hermit_time_seconds, 3),
                "pellet": round(pellet_time_seconds, 3),
                "total": round(total_time_seconds, 3),
            },
        }
        self.json_data["end_time"] = datetime.now().isoformat()
        self.json_data["iteration_count"] = iteration_count

    def save_json_log(self):
        """Save structured JSON log to file."""
        try:
            with open(self.json_log_path, "w", encoding="utf-8") as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"\n✓ Validation JSON log saved: {self.json_log_path}")
        except Exception as e:
            self.logger.error(f"Failed to save JSON log: {e}")

    def get_log_paths(self) -> Dict[str, Path]:
        """Get paths to log files."""
        return {"text_log": self.text_log_path, "json_log": self.json_log_path}
