from pydantic import BaseModel
from typing import List, Optional

class CompetencyQuestion(BaseModel):
    id: int
    question: str
    related_story_id: int
    
    def to_dict(self):
        return self.model_dump()

class Story(BaseModel):
    id: int
    context: str
    competency_questions: Optional[List[CompetencyQuestion]] = None
    
    def add_competency_question(self, cq: CompetencyQuestion):
        if self.competency_questions is None:
            self.competency_questions = []
        self.competency_questions.append(cq)
    
    def to_dict(self):
        return self.model_dump()