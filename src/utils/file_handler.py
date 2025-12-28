import glob
import os
from typing import Any, List, Tuple


def save_owl_code(owl_code: str, story_id: int, cq_id: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"story{story_id}_cq{cq_id}.owl")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(owl_code)
    return file_path


def save_combined_owl_code(owl_code: str, story_id: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"story{story_id}_combined.owl")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(owl_code)
    return file_path


def save_text_file(file_path: str, text: str) -> str:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path


def load_existing_owl_files(
    story_id: str, output_dir: str = "data/output"
) -> List[Tuple[str, str]]:
    """
    Load all existing validated OWL files for a given story.

    Args:
        story_id: The story ID (e.g., 'MusicS', 'FestS', 'HospitalS')
        output_dir: Directory where OWL files are stored

    Returns:
        List of tuples (cq_id, owl_content) for each found OWL file

    Raises:
        FileNotFoundError: If no OWL files are found for the story
    """
    # Pattern to match: {story_id}_{cq_id}.owl (not pre_validation files)
    pattern = os.path.join(output_dir, f"{story_id}_*.owl")
    owl_files = glob.glob(pattern)

    # Filter out pre_validation, concat, and combined files
    owl_files = [
        f
        for f in owl_files
        if not any(x in f for x in ["pre_validation", "concat", "combined"])
    ]

    if not owl_files:
        raise FileNotFoundError(
            f"No validated OWL files found for story '{story_id}' in {output_dir}"
        )

    # Sort files to maintain order
    owl_files.sort()

    processed_owls = []
    for file_path in owl_files:
        # Extract CQ ID from filename: {story_id}_{cq_id}.owl
        filename = os.path.basename(file_path)
        cq_id = filename.replace(f"{story_id}_", "").replace(".owl", "")

        # Read the OWL content
        with open(file_path, "r", encoding="utf-8") as f:
            owl_content = f.read()

        processed_owls.append((cq_id, owl_content))

    print(f"Loaded {len(processed_owls)} existing OWL files for story '{story_id}':")
    for cq_id, _ in processed_owls:
        print(f"  - {cq_id}")

    return processed_owls
