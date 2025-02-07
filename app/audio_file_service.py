import os
import torch
import whisper
from datetime import datetime
from app.consts import MODELS_DIR
from app.gpt_asistant_service import check_level_from_gpt_client
from app.models import language_level, language_level_create_or_update, status_enum
from app.database_service import get_language_level, get_question_content_by_language_with_id, update_language_level


async def process_audio_file(
    audio_file_id: str | int,
    WHISPER_MODEL_NAME: str,
    WHISPER_VERBOSE: str,
    WHISPER_FP16: str,
    GPT_API_KEY: str,
) -> None:
    try:
        print("Protses boshlandi")
        audio_file_id = int(audio_file_id)
        audio_file = get_language_level(audio_file_id)
        print("Audio faylni uje oldik")

        if not audio_file:
            print(f"Audio file not found in database. Id is {audio_file_id}")

        print("Transkripsiya boshlanvotti")
        transcription = await transcribe_audio(
            audio_file,
            audio_file.language,
            WHISPER_MODEL_NAME,
            WHISPER_VERBOSE,
            WHISPER_FP16,
        )

        print("Transkripsiya tugadi uje")
        language_level = {
            "language": audio_file.language,
            "question_id": audio_file.question_id,
            "file_name": audio_file.file_name,
            "full_path": audio_file.full_path,
            "status": status_enum.Transcribed,
            "transcribe_text": transcription,
            "level": audio_file.level,
            "grammatic_exceptions": audio_file.grammatic_exceptions,
            "grammatic_exceptions_score": audio_file.grammatic_exceptions_score,
            "lexical_weaknesses": audio_file.lexical_weaknesses,
            "lexical_weaknesses_score": audio_file.lexical_weaknesses_score,
            "additional_comments": audio_file.additional_comments,
            "pragmatic_context": audio_file.additional_comments,
            "pragmatic_context_score": audio_file.pragmatic_context_score,
            "stylistic_appropriateness": audio_file.stylistic_appropriateness,
            "stylistic_appropriateness_score": audio_file.stylistic_appropriateness_score,
            "vocabulary_diversity": audio_file.vocabulary_diversity,
            "vocabulary_diversity_score": audio_file.vocabulary_diversity_score,
            "sentence_complexity": audio_file.sentence_complexity,
            "sentence_complexity_score": audio_file.sentence_complexity_score,
            "engagement_level": audio_file.engagement_level,
            "engagement_level_score": audio_file.engagement_level_score,
            "tone_and_sentiment": audio_file.tone_and_sentiment,
            "tone_and_sentiment_score": audio_file.tone_and_sentiment_score,
            "overall_score": audio_file.overall_score,
            "created_at": audio_file.created_at,
            "updated_at": datetime.now(),
        }

        view_model = language_level_create_or_update(**language_level)
        update_language_level(audio_file_id, view_model)

        print("Savolni olishni boshladik")
        question_content = get_question_content_by_language_with_id(
            audio_file.language, audio_file.question_id
        )
        print("Savolni olishni tugatdik")

        print("GPT dan zapros tashadik")
        language_level_data = await check_level_from_gpt_client(
            audio_file.language,
            transcription,
            question_content,
            GPT_API_KEY,
        )
        print("GPT dan zapros keldi")

        language_level = {
            "language": audio_file.language,
            "question_id": audio_file.question_id,
            "file_name": audio_file.file_name,
            "full_path": audio_file.full_path,
            "status": status_enum.Checked,
            "transcribe_text": transcription,
            "level": language_level_data["level"],
            "grammatic_exceptions": language_level_data["grammatic_exceptions"],
            "grammatic_exceptions_score": language_level_data["grammatic_exceptions_score"],
            "lexical_weaknesses": language_level_data["lexical_weaknesses"],
            "lexical_weaknesses_score": language_level_data["lexical_weaknesses_score"],
            "additional_comments": language_level_data["additional_comments"],
            "pragmatic_context": language_level_data["pragmatic_context"],
            "pragmatic_context_score": language_level_data["pragmatic_context_score"],
            "stylistic_appropriateness": language_level_data["stylistic_appropriateness"],
            "stylistic_appropriateness_score": language_level_data["stylistic_appropriateness_score"],
            "vocabulary_diversity": language_level_data["vocabulary_diversity"],
            "vocabulary_diversity_score": language_level_data["vocabulary_diversity_score"],
            "sentence_complexity": language_level_data["sentence_complexity"],
            "sentence_complexity_score": language_level_data["sentence_complexity_score"],
            "engagement_level": language_level_data["engagement_level"],
            "engagement_level_score": language_level_data["engagement_level_score"],
            "tone_and_sentiment": language_level_data["tone_and_sentiment"],
            "tone_and_sentiment_score": language_level_data["tone_and_sentiment_score"],
            "overall_score": language_level_data["overall_score"],
            "created_at": audio_file.created_at,
            "updated_at": datetime.now(),
        }

        print("Malumotlarni o'zgartirishni boshladik, GPt dan kegin")
        view_model = language_level_create_or_update(**language_level)
        update_language_level(audio_file_id, view_model)
        print("Protses yakunlandi")
    except Exception as ex:
        print(f"Exception for {audio_file_id}, message: {ex}")


async def transcribe_audio(
    audio_file: language_level,
    language: str,
    WHISPER_MODEL_NAME: str,
    WHISPER_VERBOSE: str,
    WHISPER_FP16: str,
) -> str:
    model = whisper.load_model(name=WHISPER_MODEL_NAME, download_root=MODELS_DIR).to(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    verbose = bool(WHISPER_VERBOSE)
    fp16 = bool(WHISPER_FP16)

    audio_file_path = audio_file.full_path
    file_path = os.path.abspath(audio_file_path)
    transcription = model.transcribe(
        audio=str(file_path), language=language, verbose=verbose, fp16=fp16
    )

    return transcription["text"]
