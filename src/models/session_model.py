from pydantic import BaseModel
from typing import List

class UserSession(BaseModel):
    ability_score: float = 0.5
    num_questions: int = 0
    asked_questions: List[str] = []
    responses: List[dict] = []