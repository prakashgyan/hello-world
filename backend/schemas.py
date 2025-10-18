from pydantic import BaseModel
from typing import List

class MeaningSchema(BaseModel):
    text: str

class WordSchema(BaseModel):
    text: str
    meanings: List[MeaningSchema]

class CardSchema(BaseModel):
    word: str
    meanings: List[str]
    due_date: str

class AnswerSchema(BaseModel):
    card_id: int
    quality: int

class StatsSchema(BaseModel):
    total_words: int
    correct_percentage: float
    trend: str
