import pandas as pd
from typing import List
from src.models.requirement_models import Story, CompetencyQuestion


def extract_stories_and_cqs(excel_path: str) -> List[Story]:
    df = pd.read_excel(excel_path)
    # Assumes columns: 'StoryID', 'StoryContext', 'CQID', 'CQText'
    stories = {}
    for _, row in df.iterrows():
        story_id = int(row['StoryID'])
        if story_id not in stories:
            stories[story_id] = Story(
                id=story_id,
                context=row['StoryContext']
            )
        cq = CompetencyQuestion(
            id=int(row['CQID']),
            question=row['CQText'],
            related_story_id=story_id
        )
        stories[story_id].add_competency_question(cq)
    return list(stories.values())