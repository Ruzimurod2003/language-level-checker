import os
import shutil
import uuid

import requests


audio_extensions = {
    "wav",
    "mp3",
    "aac",
    "flac",
    "alac",
    "ogg",
    "wma",
    "aiff",
    "m4a",
    "m4b",
    "m4p",
    "mid",
    "midi",
    "mpc",
    "opus",
    "oga",
    "mp4",
}


def is_audio_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in audio_extensions


def save_file(file, upload_dir) -> tuple[str, str]:
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(unique_filename), str(file_path)


def file_download_and_save(file_url: str, upload_dir: str) -> tuple[str, str]:
    original_filename = os.path.basename(file_url)
    file_extension = os.path.splitext(original_filename)[1] or ".oga"

    unique_filename = f"{uuid.uuid4()}{file_extension}"
    save_path = os.path.join(upload_dir, unique_filename)

    response = requests.get(file_url, stream=True)
    
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        return unique_filename, save_path
    else:
        raise Exception(f"Fayl yuklab olinmadi. HTTP status kodi: {response.status_code}")
