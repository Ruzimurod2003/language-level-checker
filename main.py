import mimetypes
import os
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager
from app.rabbitmq_service import send_queue
from app.consts import API_KEY, APP_HOST, APP_PORT, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, RABBITMQ_USER, UPLOAD_DIR
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.models import language_level, language_level_create_or_update, status_enum
from app.database_service import create_language_level, get_language_level, get_language_levels, get_question_content_by_language_with_id, get_random_questions_by_language, init_db
from app.utils import file_download_and_save, is_audio_file, save_file


description = "This project is designed to determine language proficiency from audio files. It analyzes the audio using Whisper for transcription and ChatGPT for advanced linguistic analysis."

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Language level checker",
    description=description,
    version="V1.0",
    docs_url="/language_level_checker",
    openapi_url="/language_level_checker/openapi.json",
    lifespan=lifespan,
)

api_key_header = APIKeyHeader(name="api-key", auto_error=False)


def get_api_key(key_header: str = Depends(api_key_header)):
    if key_header is None or key_header != API_KEY:
        raise HTTPException(status_code=401)
    return key_header


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    path="/language_level_checker/api/upload-audio-from-url",
    tags=["Checker"],
    response_description="Upload an audio from url file for processing",
    summary="Upload an audio file from url for a specific question",
    status_code=201,
    response_model=language_level | None,
)
async def upload_audio_from_url_server_endpoint(
    language: str,
    question_id: int,
    audio_file_path: str,
    api_key: str = Depends(get_api_key),
):
    try:
        unique_filename, file_path = file_download_and_save(audio_file_path, UPLOAD_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving error: {str(e)}")
    

    language_level = {
        "language": language,
        "question_id": question_id,
        "file_name": unique_filename,
        "full_path": file_path,
        "status": status_enum.Saved,
        "transcribe_text": None,
        "level": None,
        "grammatic_exceptions": None,
        "grammatic_exceptions_score": None,
        "lexical_weaknesses": None,
        "lexical_weaknesses_score": None,
        "additional_comments": None,
        "pragmatic_context": None,
        "pragmatic_context_score": None,
        "stylistic_appropriateness": None,
        "stylistic_appropriateness_score": None,
        "vocabulary_diversity": None,
        "vocabulary_diversity_score": None,
        "sentence_complexity": None,
        "sentence_complexity_score": None,
        "engagement_level": None,
        "engagement_level_score": None,
        "tone_and_sentiment": None,
        "tone_and_sentiment_score": None,
        "overall_score": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    last_row_id = create_language_level(
        language_level_create_or_update(**language_level)
    )
    db_language_level = get_language_level(last_row_id)

    db_language_level.question_content = get_question_content_by_language_with_id(
        db_language_level.language, db_language_level.question_id
    )

    await send_queue(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, last_row_id)

    return db_language_level


@app.post(
    path="/language_level_checker/api/upload-audio",
    tags=["Checker"],
    response_description="Upload an audio file for processing",
    summary="Upload an audio file for a specific question",
    status_code=201,
    response_model=language_level | None,
)
async def upload_audio_endpoint(
    language: str,
    question_id: int,
    audio_file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
):
    if not is_audio_file(audio_file.filename):
        raise HTTPException(status_code=400, detail="Invalid audio file format")
    
    try:
        unique_filename, file_path = save_file(audio_file, UPLOAD_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving error: {str(e)}")
    

    language_level = {
        "language": language,
        "question_id": question_id,
        "file_name": unique_filename,
        "full_path": file_path,
        "status": status_enum.Saved,
        "transcribe_text": None,
        "level": None,
        "grammatic_exceptions": None,
        "grammatic_exceptions_score": None,
        "lexical_weaknesses": None,
        "lexical_weaknesses_score": None,
        "additional_comments": None,
        "pragmatic_context": None,
        "pragmatic_context_score": None,
        "stylistic_appropriateness": None,
        "stylistic_appropriateness_score": None,
        "vocabulary_diversity": None,
        "vocabulary_diversity_score": None,
        "sentence_complexity": None,
        "sentence_complexity_score": None,
        "engagement_level": None,
        "engagement_level_score": None,
        "tone_and_sentiment": None,
        "tone_and_sentiment_score": None,
        "overall_score": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    last_row_id = create_language_level(
        language_level_create_or_update(**language_level)
    )
    db_language_level = get_language_level(last_row_id)

    db_language_level.question_content = get_question_content_by_language_with_id(
        db_language_level.language, db_language_level.question_id
    )

    await send_queue(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, last_row_id)

    return db_language_level


@app.get(
    path="/language_level_checker/api/get-language-level",
    tags=["Checker"],
    response_description="Retrieve a single language level with its audio question",
    summary="Fetch a specific language level for manual processing",
    status_code=201,
    response_model=language_level | None,
)
async def get_audio_endpoint(
    language_level_id: int, api_key: str = Depends(get_api_key)
):
    db_language_level = get_language_level(language_level_id)
    db_language_level.question_content = get_question_content_by_language_with_id(
        db_language_level.language, db_language_level.question_id
    )

    return db_language_level


@app.get(
    path="/language_level_checker/api/get-language-levels",
    tags=["Checker"],
    response_description="List of language levels with audio questions",
    summary="Retrieve language levels for manual processing",
    status_code=201,
    response_model=list[language_level] | None,
)
async def get_audio_endpoint(api_key: str = Depends(get_api_key)):
    db_language_levels = get_language_levels()
    for db_language_level in db_language_levels:
        db_language_level.question_content = get_question_content_by_language_with_id(
            db_language_level.language, db_language_level.question_id
        )
    return db_language_levels


@app.get(
    path="/language_level_checker/api/get-question",
    tags=["Checker"],
    response_description="Retrieve a random audio question by language",
    summary="Fetch random audio questions for manual processing",
    status_code=201,
)
async def get_audio_endpoint(language: str, api_key: str = Depends(get_api_key)):
    return get_random_questions_by_language(language)


@app.get(
    path="/language_level_checker/api/export-audio-file",
    tags=["Checker"],
    summary="Retrieve and download an audio file for a language level",
    response_description="Returns an audio file in either .mp3 or .ogg format based on the specified language level ID."
)
async def export_audio_file_endpoint(
    language_level_id: int,
    api_key: str = Depends(get_api_key)
):
    db_language_level = get_language_level(language_level_id)
    
    if not db_language_level or not db_language_level.full_path:
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    file_path = db_language_level.full_path

    # Fayl mavjudligini tekshiramiz
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fayl mavjud emas")
    
    # Fayl formatini MIME turi orqali aniqlash
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Agar MIME aniqlanmasa, default qilib qo'yiladi


    return FileResponse(path=file_path, media_type=mime_type, filename=os.path.basename(file_path))

if __name__ == "__main__":
    uvicorn.run(app, host=str(APP_HOST), port=int(APP_PORT))
