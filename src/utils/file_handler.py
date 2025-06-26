import os
from typing import Any

def save_owl_code(owl_code: str, story_id: int, cq_id: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"story{story_id}_cq{cq_id}.owl")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(owl_code)
    return file_path

def save_combined_owl_code(owl_code: str, story_id: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"story{story_id}_combined.owl")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(owl_code)
    return file_path

def save_text_file(file_path: str, text: str) -> str:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return file_path
