# Language Level Checker

**Language Level Checker** is a FastAPI-based web service designed to evaluate a user's language proficiency from audio files. The application uses [Whisper](https://github.com/openai/whisper) for audio transcription and leverages ChatGPT (via the OpenAI API) for advanced linguistic analysis. It supports asynchronous processing through RabbitMQ, stores metadata and evaluation results in a SQLite database, and provides several endpoints to manage and review the evaluation process.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Audio Upload Options**:  
  - Upload an audio file via multipart form data.
  - Upload an audio file by providing a URL.
  
- **Asynchronous Processing**:  
  - Saves uploaded audio files and queues them for processing using RabbitMQ.
  - A background consumer processes the files: transcribes audio with Whisper and evaluates language proficiency with ChatGPT.

- **Detailed Evaluation**:  
  - Generates a detailed evaluation including overall language level (A1, A2, B1, B2, C1, C2) and scores for specific linguistic aspects (grammar, lexical resource, pragmatic context, stylistic appropriateness, etc.).

- **Data Persistence**:  
  - Uses a SQLite database to store audio file metadata and evaluation results.

- **File Export**:  
  - Provides an endpoint to download the original audio file after processing.

---

## Architecture Overview

1. **FastAPI Server**:  
   The main web service exposes endpoints for uploading audio files, retrieving evaluation results, and exporting audio files.

2. **RabbitMQ Queue**:  
   Uploaded files are sent to a RabbitMQ queue. A background consumer listens to this queue, processes each file asynchronously, and updates the evaluation results.

3. **Whisper Transcription**:  
   The consumer uses the Whisper model to transcribe audio files.

4. **ChatGPT Evaluation**:  
   The transcribed text is sent to ChatGPT for detailed language proficiency evaluation.

5. **SQLite Database**:  
   Audio file metadata and evaluation results are stored in a SQLite database, with SQL scripts provided for table creation, data insertion, and updates.

---

## Prerequisites

- **Python 3.8+**
- **RabbitMQ Server** (for task queuing)
- **SQLite** (default database)
- **CUDA** (optional, for GPU-accelerated transcription with Whisper)
- Required Python packages (see [Installation](#installation)):
  - FastAPI
  - Uvicorn
  - Pydantic
  - Requests
  - Pika
  - Whisper
  - OpenAI Python client

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/language-level-checker.git
   cd language-level-checker
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Make sure your `requirements.txt` includes all the necessary packages such as FastAPI, Uvicorn, Pika, Requests, Whisper, and OpenAI.*

---

## Configuration

Update the configuration constants in the `app/consts.py` file (or use environment variables) to specify:

- **API Security & Server Settings**:
  - `API_KEY`: API key for securing the endpoints.
  - `APP_HOST` and `APP_PORT`: Host and port settings for the FastAPI server.

- **RabbitMQ Settings**:
  - `RABBITMQ_HOST`
  - `RABBITMQ_USER`
  - `RABBITMQ_PASSWORD`
  - `RABBITMQ_QUEUE`

- **File and Database Settings**:
  - `UPLOAD_DIR`: Directory where uploaded audio files will be stored.
  - `DATABASE_URL`: SQLite database file path.
  - `QUESTIONS_DIR`: Directory containing JSON files with audio questions.

- **Transcription and Evaluation Settings**:
  - `GPT_API_KEY`: OpenAI API key used for ChatGPT evaluations.
  - `WHISPER_MODEL_NAME`, `WHISPER_VERBOSE`, `WHISPER_FP16`: Parameters for configuring the Whisper transcription model.
  - `MODELS_DIR`: Directory for storing downloaded Whisper models.
  - `LANGUAGES`: Mapping of language codes to full language names (used in evaluation prompts).

---

## Running the Application

### 1. Start the FastAPI Server

Run the main FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

After starting, you can access the API documentation at:  
`http://<APP_HOST>:<APP_PORT>/language_level_checker`

### 2. Start the RabbitMQ Consumer

The consumer continuously listens to the RabbitMQ queue and processes audio tasks. To start the consumer, run:

```bash
python consumer.py
```

*The consumer uses an infinite loop to listen for new messages, process audio files asynchronously (transcription and evaluation), and update the database accordingly.*

---

## API Endpoints

### Upload Audio from URL

- **Endpoint**: `POST /language_level_checker/api/upload-audio-from-url`
- **Description**: Downloads an audio file from the provided URL, saves it locally, and queues it for processing.
- **Parameters**:
  - `language` (str): Language code.
  - `question_id` (int): Identifier of the audio question.
  - `audio_file_path` (str): URL of the audio file.
- **Headers**:  
  - `api-key`: Your API key.

---

### Upload Audio File

- **Endpoint**: `POST /language_level_checker/api/upload-audio`
- **Description**: Accepts an audio file (multipart/form-data), saves it, and queues it for processing.
- **Parameters**:
  - `language` (str): Language code.
  - `question_id` (int): Identifier of the audio question.
  - `audio_file` (UploadFile): The audio file to be uploaded.
- **Headers**:  
  - `api-key`: Your API key.

---

### Retrieve a Specific Language Level

- **Endpoint**: `GET /language_level_checker/api/get-language-level`
- **Description**: Retrieves the evaluation result (including transcription and analysis) for a specific audio file.
- **Parameters**:
  - `language_level_id` (int): The unique ID of the language evaluation record.
- **Headers**:  
  - `api-key`: Your API key.

---

### Retrieve All Language Levels

- **Endpoint**: `GET /language_level_checker/api/get-language-levels`
- **Description**: Retrieves a list of all language evaluation records.
- **Headers**:  
  - `api-key`: Your API key.

---

### Get a Random Audio Question

- **Endpoint**: `GET /language_level_checker/api/get-question`
- **Description**: Returns a random audio question for the specified language.
- **Parameters**:
  - `language` (str): Language code.
- **Headers**:  
  - `api-key`: Your API key.

---

### Export Audio File

- **Endpoint**: `GET /language_level_checker/api/export-audio-file`
- **Description**: Downloads the original audio file corresponding to the given evaluation record.
- **Parameters**:
  - `language_level_id` (int): The unique ID of the evaluation record.
- **Headers**:  
  - `api-key`: Your API key.

---

## Project Structure

```
language-level-checker/
├── app/
│   ├── __init__.py
│   ├── consts.py              # Configuration constants
│   ├── models.py              # Pydantic models and Enums
│   ├── database_service.py    # SQLite database operations
│   ├── rabbitmq_service.py    # RabbitMQ integration for queuing and consuming
│   ├── audio_file_service.py  # Audio file processing (transcription & evaluation)
│   ├── utils.py               # Utility functions (file saving, validation, etc.)
│   └── gpt_asistant_service.py# ChatGPT integration for linguistic evaluation
├── db/
│   ├── create_table_language_level.sql
│   ├── insert_into_language_level.sql
│   ├── update_data_language_level.sql
│   └── select_language_level.sql
├── questions/
│   └── questions.<language>.json  # JSON files containing audio questions
├── consumer.py               # RabbitMQ consumer script for processing audio tasks
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or improvements, please feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Whisper](https://github.com/openai/whisper)
- [OpenAI](https://openai.com/)
- [RabbitMQ](https://www.rabbitmq.com/)

---
