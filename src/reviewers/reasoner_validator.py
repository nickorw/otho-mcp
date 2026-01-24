"""
Reasoner-based validators for ontology consistency checking.

This module provides validators that use OWL reasoners (Hermit and Pellet)
to check logical consistency of ontologies. Both reasoners are accessed
via the Owlready2 library which bridges Python to Java-based reasoners.
"""

import gc
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

from owlready2 import World, get_ontology, sync_reasoner_hermit, sync_reasoner_pellet


class ReasonerValidator:
    """
    Base class for reasoner-based validators.

    Implements state isolation pattern to prevent contamination between
    validation runs. Each validation creates a fresh ontology world and
    explicitly cleans up afterward.
    """

    def __init__(self, reasoner_name: str):
        self.reasoner_name = reasoner_name
        self.temp_file = None

    def _get_rdfxml_path(self) -> str:
        """
        Get path to RDF/XML file created by OOPS validation.

        OOPS reviewer converts Turtle to RDF/XML and saves it to
        data/output/xml_combined_owl.xml. Since reasoners run after
        OOPS in the validation pipeline, we can reuse this file.

        Returns:
            Path to RDF/XML file
        """
        return "data/output/xml_combined_owl.xml"

    def _cleanup_temp_file(self):
        """Delete temporary file if it exists."""
        if self.temp_file:
            try:
                Path(self.temp_file.name).unlink(missing_ok=True)
            except Exception as e:
                print(f"Warning: Could not delete temp file: {e}")
            finally:
                self.temp_file = None

    def _run_reasoner(self, onto, reasoner_func) -> Dict[str, Any]:
        """
        Run reasoner and capture results.

        Args:
            onto: Owlready2 ontology object
            reasoner_func: Function to call (sync_reasoner_hermit or sync_reasoner_pellet)

        Returns:
            Dict with consistency results and any errors found
        """
        start_time = time.time()

        try:
            # Run the reasoner - this performs consistency checking
            reasoner_func(onto, infer_property_values=True, debug=0)

            # Check for inconsistencies
            inconsistent_classes = list(onto.inconsistent_classes())

            elapsed_seconds = time.time() - start_time

            return {
                "is_consistent": len(inconsistent_classes) == 0,
                "inconsistent_classes": [str(c) for c in inconsistent_classes],
                "execution_time_seconds": round(elapsed_seconds, 3),
                "error": None,
            }

        except Exception as e:
            elapsed_seconds = time.time() - start_time
            return {
                "is_consistent": False,
                "inconsistent_classes": [],
                "execution_time_seconds": round(elapsed_seconds, 3),
                "error": str(e),
            }

    def validate(self) -> Dict[str, Any]:
        """
        Validate ontology consistency using RDF/XML file from OOPS.

        Returns:
            Validation results dictionary
        """
        raise NotImplementedError("Subclasses must implement validate()")

    def _cleanup(self):
        """
        Perform cleanup to ensure state isolation.

        This is critical to prevent state contamination between validator runs.
        Forces garbage collection to clean up JVM objects.
        """
        self._cleanup_temp_file()
        gc.collect()  # Force garbage collection to clean up JVM objects


class HermitReasonerValidator(ReasonerValidator):
    """
    Validator using the Hermit OWL reasoner.

    Hermit is a highly optimized OWL 2 DL reasoner known for speed
    and correctness. It uses hypertableau calculus for reasoning.
    """

    def __init__(self):
        super().__init__("Hermit")

    def validate(self) -> Dict[str, Any]:
        """
        Validate ontology consistency using Hermit reasoner.

        Reads RDF/XML file created by OOPS validation pipeline.
        Uses explicit world isolation to prevent state contamination.

        Returns:
            {
                "reasoner": "Hermit",
                "is_consistent": bool,
                "inconsistent_classes": list of class URIs,
                "execution_time_seconds": float,
                "error": str or None
            }
        """
        # Create isolated world for this validation
        world = World()

        try:
            # Get RDF/XML file path (created by OOPS validation)
            rdfxml_path = self._get_rdfxml_path()

            # Check if file exists
            if not Path(rdfxml_path).exists():
                return {
                    "reasoner": self.reasoner_name,
                    "is_consistent": False,
                    "inconsistent_classes": [],
                    "execution_time_seconds": 0.0,
                    "error": f"RDF/XML file not found: {rdfxml_path}. OOPS must run first.",
                }

            # Load ontology into isolated world
            onto = world.get_ontology(f"file://{rdfxml_path}").load()

            # Run Hermit reasoner in isolated world
            result = self._run_reasoner(onto, sync_reasoner_hermit)

            # Add reasoner name
            result["reasoner"] = self.reasoner_name

            return result

        except Exception as e:
            return {
                "reasoner": self.reasoner_name,
                "is_consistent": False,
                "inconsistent_classes": [],
                "execution_time_seconds": 0.0,
                "error": f"Failed to load or validate ontology: {str(e)}",
            }

        finally:
            # Destroy world to ensure complete cleanup
            try:
                world.close()
            except:
                pass  # World may already be closed or not fully initialized

            # Always cleanup to ensure state isolation
            self._cleanup()


class PelletReasonerValidator(ReasonerValidator):
    """
    Validator using the Pellet OWL reasoner.

    Pellet is a complete and capable OWL 2 DL reasoner with excellent
    support for SWRL rules and OWL 2 features.
    """

    def __init__(self):
        super().__init__("Pellet")

    def validate(self) -> Dict[str, Any]:
        """
        Validate ontology consistency using Pellet reasoner.

        Reads RDF/XML file created by OOPS validation pipeline.
        Uses explicit world isolation to prevent state contamination.

        Returns:
            {
                "reasoner": "Pellet",
                "is_consistent": bool,
                "inconsistent_classes": list of class URIs,
                "execution_time_seconds": float,
                "error": str or None
            }
        """
        # Create isolated world for this validation
        world = World()

        try:
            # Get RDF/XML file path (created by OOPS validation)
            rdfxml_path = self._get_rdfxml_path()

            # Check if file exists
            if not Path(rdfxml_path).exists():
                return {
                    "reasoner": self.reasoner_name,
                    "is_consistent": False,
                    "inconsistent_classes": [],
                    "execution_time_seconds": 0.0,
                    "error": f"RDF/XML file not found: {rdfxml_path}. OOPS must run first.",
                }

            # Load ontology into isolated world
            onto = world.get_ontology(f"file://{rdfxml_path}").load()

            # Run Pellet reasoner in isolated world
            result = self._run_reasoner(onto, sync_reasoner_pellet)

            # Add reasoner name
            result["reasoner"] = self.reasoner_name

            return result

        except Exception as e:
            return {
                "reasoner": self.reasoner_name,
                "is_consistent": False,
                "inconsistent_classes": [],
                "execution_time_seconds": 0.0,
                "error": f"Failed to load or validate ontology: {str(e)}",
            }

        finally:
            # Destroy world to ensure complete cleanup
            try:
                world.close()
            except:
                pass  # World may already be closed or not fully initialized

            # Always cleanup to ensure state isolation
            self._cleanup()


def validate_with_reasoners() -> Dict[str, Dict[str, Any]]:
    """
    Validate ontology with both Hermit and Pellet reasoners.

    Runs both reasoners sequentially with proper state isolation.
    Each reasoner gets a fresh environment to prevent contamination.

    Reads RDF/XML file created by OOPS validation (data/output/xml_combined_owl.xml).

    Returns:
        {
            "hermit": {...hermit results...},
            "pellet": {...pellet results...}
        }
    """
    hermit = HermitReasonerValidator()
    pellet = PelletReasonerValidator()

    return {
        "hermit": hermit.validate(),
        "pellet": pellet.validate(),
    }
