from typing import NoReturn
from app.consts import GPT_API_KEY, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, RABBITMQ_USER, WHISPER_FP16, WHISPER_MODEL_NAME, WHISPER_VERBOSE
from app.rabbitmq_service import get_queue


def start_consumer() -> NoReturn:
    get_queue(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, WHISPER_MODEL_NAME, WHISPER_VERBOSE, WHISPER_FP16, GPT_API_KEY)

if __name__ == "__main__":
    start_consumer()
