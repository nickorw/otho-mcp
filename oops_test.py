from src.reviewers.reviewer import OopsPitfallReviewer

pitfall_reviewer = OopsPitfallReviewer()
result = pitfall_reviewer.review_owl_file(
    owl_file_path="data/output/xml_combined_owl.xml",
    output_format="XML",
)
print("Pitfall Validation Result:", result)