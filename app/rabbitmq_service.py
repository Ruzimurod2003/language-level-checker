import time
import pika
import asyncio
from app.audio_file_service import process_audio_file


async def send_queue(
    RABBITMQ_HOST: str,
    RABBITMQ_USER: str,
    RABBITMQ_PASSWORD: str,
    RABBITMQ_QUEUE: str,
    message: str,
) -> None:
    try:
        credentials = pika.PlainCredentials(
            username=str(RABBITMQ_USER),
            password=str(RABBITMQ_PASSWORD),
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=str(RABBITMQ_HOST), credentials=credentials)
        )
        channel = connection.channel()
        queue_name = str(RABBITMQ_QUEUE)
        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange="", routing_key=queue_name, body=str(message))
    except Exception as e:
        print(f"Exception - {str(e)}")


def get_queue(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE, WHISPER_MODEL_NAME, WHISPER_VERBOSE, WHISPER_FP16, GPT_API_KEY):
    while True:
        try:
            print("Rabbitga ulanish boshlanvotti")
            credentials = pika.PlainCredentials(
                username=str(RABBITMQ_USER),
                password=str(RABBITMQ_PASSWORD),
            )

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=str(RABBITMQ_HOST),
                    credentials=credentials,
                    heartbeat=0,
                )
            )

            channel = connection.channel()
            queue_name = str(RABBITMQ_QUEUE)
            channel.queue_declare(queue=queue_name)

            def callback(ch, method, properties, body):
                audio_file_id = body.decode()
                try:
                    print("Metodga uzatvomiza")
                    asyncio.run(
                        process_audio_file(
                            str(audio_file_id),
                            WHISPER_MODEL_NAME,
                            WHISPER_VERBOSE,
                            WHISPER_FP16,
                            GPT_API_KEY,
                        )
                    )
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            # channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=False,
            )

            channel.start_consuming()
        except Exception as ex:
            print(ex)
            time.sleep(1)
