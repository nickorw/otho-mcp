import pandas as pd
from typing import List
from src.models.requirement_models import Story, CompetencyQuestion

DATASET_PATH = "data/input/OthoDataset.xlsx"


def extract_stories_and_cqs() -> List[Story]:
    df = pd.read_excel(DATASET_PATH)
    # Assumes columns: 'StoryID', 'StoryContext', 'CQID', 'CQText'
    stories = {}
    for _, row in df.iterrows():
        if pd.isna(row['StoryID']):
            continue  # Skip rows with missing StoryID
        story_id = str(row['StoryID'])
        if story_id not in stories:
            stories[story_id] = Story(
                id=story_id,
                context=row['StoryContext']
            )
        if pd.isna(row['CQID']) or pd.isna(row['CQText']):
            continue  # Skip rows with missing CQID or CQText
        cq = CompetencyQuestion(
            id=str(row['CQID']),
            question=row['CQText'],
            related_story_id=story_id
        )
        stories[story_id].add_competency_question(cq)
    return list(stories.values())


def get_cqs_for_story(story_id: str) -> list:
    df = pd.read_excel(DATASET_PATH)
    cqs = []
    for _, row in df.iterrows():
        if pd.isna(row['StoryID']) or str(row['StoryID']) != story_id:
            continue
        if pd.isna(row['CQID']) or pd.isna(row['CQText']):
            continue
        cq = CompetencyQuestion(
            id=str(row['CQID']),
            question=row['CQText'],
            related_story_id=story_id
        )
        cqs.append(cq)
    return cqs


def get_story_text_for_id(story_id: str) -> str:
    df = pd.read_excel(DATASET_PATH, sheet_name='Story')
    for _, row in df.iterrows():
        if pd.isna(row['StoryID']):
            continue
        if str(row['StoryID']) == story_id:
            return str(row['StoryText'])
    return ""


def get_story_by_id(story_id: str) -> Story:
    story_text = get_story_text_for_id(story_id)
    cqs = get_cqs_for_story(story_id)
    return Story(id=story_id, context=story_text, competency_questions=cqs)