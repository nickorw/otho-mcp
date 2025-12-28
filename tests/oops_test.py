import os
import sys
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.reviewers.reviewer import OopsPitfallReviewer

# Get the project root directory
project_root = Path(__file__).parent.parent

pitfall_reviewer = OopsPitfallReviewer()
pitfalls = [
    "2,3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 19, 20, 21, 22, 24, 25, 25, 26, 27, 28, 29"
]

# Use absolute path from project root
owl_file_path = project_root / "data" / "output" / "xml_combined_owl.xml"

result = pitfall_reviewer.review_owl_file(
    owl_file_path=str(owl_file_path),
    pitfalls=pitfalls,
    output_format="XML",
)
print("Pitfall Validation Result:", result)


# pitfall_reviewer = OopsPitfallReviewer()
# owl_file_path = os.path.join(
#     "data",
#     "output",
#     "Backup",
#     "FestS_combined_turtle.owl",
# )

# with open(owl_file_path, "r", encoding="utf-8") as f:
#     owl_content = f.read()


# pitfalls = [
#     "2,3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 19, 20, 21, 22, 24, 25, 25, 26, 27, 28, 29"
# ]
# # Act
# result = pitfall_reviewer.review_owl_content(
#     owl_content, pitfalls=pitfalls, output_format="XML"
# )
# print("review_owl_content_real_api result:", result)
