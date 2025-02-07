from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class status_enum(Enum):
    Saved = 1
    Transcribed = 2
    Checked = 3


class level_enum(Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class language_level(BaseModel):
    id: int
    language: str
    question_id: int
    question_content: Optional[str]
    file_name: str
    full_path: str
    status: status_enum
    transcribe_text: Optional[str]
    level: Optional[level_enum]
    grammatic_exceptions: Optional[str]
    grammatic_exceptions_score: Optional[float]
    lexical_weaknesses: Optional[str]
    lexical_weaknesses_score: Optional[float]
    additional_comments: Optional[str]
    pragmatic_context: Optional[str]
    pragmatic_context_score: Optional[float]
    stylistic_appropriateness: Optional[str]
    stylistic_appropriateness_score: Optional[float]
    vocabulary_diversity: Optional[str]
    vocabulary_diversity_score: Optional[float]
    sentence_complexity: Optional[str]
    sentence_complexity_score: Optional[float]
    engagement_level: Optional[str]
    engagement_level_score: Optional[float]
    tone_and_sentiment: Optional[str]
    tone_and_sentiment_score: Optional[float]
    overall_score: Optional[float]
    created_at: datetime
    updated_at: datetime


class language_level_create_or_update(BaseModel):
    language: str
    question_id: int
    file_name: str
    full_path: str
    status: status_enum
    transcribe_text: Optional[str]
    level: Optional[level_enum]
    grammatic_exceptions: Optional[str]
    grammatic_exceptions_score: Optional[float]
    lexical_weaknesses: Optional[str]
    lexical_weaknesses_score: Optional[float]
    additional_comments: Optional[str]
    pragmatic_context: Optional[str]
    pragmatic_context_score: Optional[float]
    stylistic_appropriateness: Optional[str]
    stylistic_appropriateness_score: Optional[float]
    vocabulary_diversity: Optional[str]
    vocabulary_diversity_score: Optional[float]
    sentence_complexity: Optional[str]
    sentence_complexity_score: Optional[float]
    engagement_level: Optional[str]
    engagement_level_score: Optional[float]
    tone_and_sentiment: Optional[str]
    tone_and_sentiment_score: Optional[float]
    overall_score: Optional[float]
    created_at: datetime
    updated_at: datetime
