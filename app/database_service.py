import os
import json
import random
import sqlite3
from typing import Any
from contextlib import contextmanager
from app.consts import DATABASE_URL, QUESTIONS_DIR
from app.models import language_level, language_level_create_or_update


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with open(os.path.join("db", "create_table_language_level.sql"), "r") as f:
        sql_script = f.read()
    with get_db_connection() as conn:
        conn.executescript(sql_script)
        conn.commit()


def create_language_level(language_level: language_level_create_or_update) -> int:
    with open(os.path.join("db", "insert_into_language_level.sql"), "r") as f:
        sql_script = f.read()
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            sql_script,
            (
                language_level.language,
                language_level.question_id,
                language_level.file_name,
                language_level.full_path,
                language_level.status.value
                if language_level.status is not None
                else None,
                language_level.transcribe_text,
                language_level.level.value
                if language_level.level is not None
                else None,
                language_level.grammatic_exceptions,
                language_level.grammatic_exceptions_score,
                language_level.lexical_weaknesses,
                language_level.lexical_weaknesses_score,
                language_level.additional_comments,
                language_level.pragmatic_context,
                language_level.pragmatic_context_score,
                language_level.stylistic_appropriateness,
                language_level.stylistic_appropriateness_score,
                language_level.vocabulary_diversity,
                language_level.vocabulary_diversity_score,
                language_level.sentence_complexity,
                language_level.sentence_complexity_score,
                language_level.engagement_level,
                language_level.engagement_level_score,
                language_level.tone_and_sentiment,
                language_level.tone_and_sentiment_score,
                language_level.overall_score,
                language_level.created_at,
                language_level.updated_at,
            ),
        )
        conn.commit()
        return cur.lastrowid


def update_language_level(
    id: int, updated_language_level: language_level_create_or_update
):
    with open(os.path.join("db", "update_data_language_level.sql"), "r") as f:
        sql_script = f.read()
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            sql_script,
            (
                updated_language_level.language,
                updated_language_level.question_id,
                updated_language_level.file_name,
                updated_language_level.full_path,
                updated_language_level.status.value
                if updated_language_level.status is not None
                else None,
                updated_language_level.transcribe_text,
                updated_language_level.level.value
                if updated_language_level.level is not None
                else None,
                updated_language_level.grammatic_exceptions,
                updated_language_level.grammatic_exceptions_score,
                updated_language_level.lexical_weaknesses,
                updated_language_level.lexical_weaknesses_score,
                updated_language_level.additional_comments,
                updated_language_level.pragmatic_context,
                updated_language_level.pragmatic_context_score,
                updated_language_level.stylistic_appropriateness,
                updated_language_level.stylistic_appropriateness_score,
                updated_language_level.vocabulary_diversity,
                updated_language_level.vocabulary_diversity_score,
                updated_language_level.sentence_complexity,
                updated_language_level.sentence_complexity_score,
                updated_language_level.engagement_level,
                updated_language_level.engagement_level_score,
                updated_language_level.tone_and_sentiment,
                updated_language_level.tone_and_sentiment_score,
                updated_language_level.overall_score,
                updated_language_level.created_at,
                updated_language_level.updated_at,
                id,
            ),
        )
        conn.commit()


def get_language_level(id: int) -> language_level | None:
    with open(os.path.join("db", "select_language_level.sql"), "r") as f:
        sql_script = f.read()
    with get_db_connection() as conn:
        cur = conn.cursor()
        data = cur.execute(sql_script, (id,)).fetchone()
        if data:
            return language_level(
                id=data[0],
                language=data[1],
                question_id=data[2],
                file_name=data[3],
                full_path=data[4],
                status=data[5],
                transcribe_text=data[6],
                level=data[7],
                grammatic_exceptions=data[8],
                grammatic_exceptions_score=data[9],
                lexical_weaknesses=data[10],
                lexical_weaknesses_score=data[11],
                additional_comments=data[12],
                pragmatic_context=data[13],
                pragmatic_context_score=data[14],
                stylistic_appropriateness=data[15],
                stylistic_appropriateness_score=data[16],
                vocabulary_diversity=data[17],
                vocabulary_diversity_score=data[18],
                sentence_complexity=data[19],
                sentence_complexity_score=data[20],
                engagement_level=data[21],
                engagement_level_score=data[22],
                tone_and_sentiment=data[23],
                tone_and_sentiment_score=data[24],
                overall_score=data[25],
                created_at=data[26],
                updated_at=data[27],
                question_content=None,
            )
        return None


def get_language_levels() -> list[language_level]:
    with open(os.path.join("db", "select_all_language_levels.sql"), "r") as f:
        sql_script = f.read()
    with get_db_connection() as conn:
        cur = conn.cursor()
        dublicate_language_levels = cur.execute(sql_script).fetchall()
    result = []
    for dublicate_language_level in dublicate_language_levels:
        result.append(
            language_level(
                id=dublicate_language_level[0],
                language=dublicate_language_level[1],
                question_id=dublicate_language_level[2],
                file_name=dublicate_language_level[3],
                full_path=dublicate_language_level[4],
                status=dublicate_language_level[5],
                transcribe_text=dublicate_language_level[6],
                level=dublicate_language_level[7],
                grammatic_exceptions=dublicate_language_level[8],
                grammatic_exceptions_score=dublicate_language_level[9],
                lexical_weaknesses=dublicate_language_level[10],
                lexical_weaknesses_score=dublicate_language_level[11],
                additional_comments=dublicate_language_level[12],
                pragmatic_context=dublicate_language_level[13],
                pragmatic_context_score=dublicate_language_level[14],
                stylistic_appropriateness=dublicate_language_level[15],
                stylistic_appropriateness_score=dublicate_language_level[16],
                vocabulary_diversity=dublicate_language_level[17],
                vocabulary_diversity_score=dublicate_language_level[18],
                sentence_complexity=dublicate_language_level[19],
                sentence_complexity_score=dublicate_language_level[20],
                engagement_level=dublicate_language_level[21],
                engagement_level_score=dublicate_language_level[22],
                tone_and_sentiment=dublicate_language_level[23],
                tone_and_sentiment_score=dublicate_language_level[24],
                overall_score=dublicate_language_level[25],
                created_at=dublicate_language_level[26],
                updated_at=dublicate_language_level[27],
                question_content=None,
            )
        )
    return result


def get_random_questions_by_language(language: str) -> Any | None:
    file_path = os.path.join(QUESTIONS_DIR, f"questions.{language}.json")
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        question_ids = [question["question_id"] for question in data]
        selected_id = random.choice(question_ids)

        for question in data:
            if question["question_id"] == selected_id:
                return question
    return None


def get_question_content_by_language_with_id(language: str, question_id: int) -> str | None:
    file_path = os.path.join(QUESTIONS_DIR, f"questions.{language}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for question in data:
            if question["question_id"] == question_id:
                return question["question_content"]
    return None
