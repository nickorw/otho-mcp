import glob
import os


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


def load_story_owl(story_id: str, output_dir: str = "data/output") -> str:
    """
    Load the ontology OWL file for a story.

    Returns:
        OWL file content as a string

    Raises:
        FileNotFoundError: If no OWL file is found
    """

    # Pattern for the single ontology file: {story_id}_ontology_{timestamp}.owl
    pattern = os.path.join(output_dir, f"{story_id}_ontology_*.owl")
    matches = glob.glob(pattern)

    if not matches:
        raise FileNotFoundError(
            f"No ontology OWL file found for story '{story_id}' in {output_dir}"
        )

    # Pick the most recent file if multiple exist
    matches.sort(key=os.path.getmtime, reverse=True)
    file_path = matches[0]

    with open(file_path, "r", encoding="utf-8") as f:
        owl_content = f.read()

    print(
        f"Loaded ontology OWL file for story '{story_id}': {os.path.basename(file_path)}"
        + (" (picked latest)" if len(matches) > 1 else "")
    )

    return owl_content
