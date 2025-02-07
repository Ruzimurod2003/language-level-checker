INSERT INTO language_levels (
    language,
    question_id,
    file_name,
    full_path,
    status,
    transcribe_text,
    level,
    grammatic_exceptions,
    grammatic_exceptions_score,
    lexical_weaknesses,
    lexical_weaknesses_score,
    additional_comments,
    pragmatic_context,
    pragmatic_context_score,
    stylistic_appropriateness,
    stylistic_appropriateness_score,
    vocabulary_diversity,
    vocabulary_diversity_score,
    sentence_complexity,
    sentence_complexity_score,
    engagement_level,
    engagement_level_score,
    tone_and_sentiment,
    tone_and_sentiment_score,
    overall_score,
    created_at,
    updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);