import json
from typing import Any
from openai import OpenAI
from app.consts import LANGUAGES


async def add_new_questions_not_exists(language: str, GPT_API_KEY: str) -> Any:
    language_full = LANGUAGES[f"{language}"]
    prompt = (
        "I need a list of 100 questions for an interview to determine the user's language proficiency, can you provide me with this in JSON format?"
        f"Language to create questions: {language_full}"
        """In JSON format:
        [
            { question_id: number, question_content: text },
            { question_id: number, question_content: text },
        ]"""
        "question_id will be 1, 2, 3 ..."
    )

    data_from_ai = await connect_gpt_client_and_send_message(prompt, GPT_API_KEY)

    language_level_data = json.loads(data_from_ai)

    return language_level_data


async def check_level_from_gpt_client(
    language: str, transcribe_text: str, question_content: str, GPT_API_KEY: str
) -> Any:
    prompt = (
        f"We need to evaluate the user's language proficiency. Below are the details:\n"
        f"Language: {language}\n"
        f"Question content: {question_content}\n"
        f"User's answer to this question: {transcribe_text}\n\n"
        "The evaluation should be based on the following fields, with score values ranging from 0-100%.\n"
        "Return the result in the exact JSON format shown below:\n"
        """{
            "level": "str", # One of {A1, A2, B1, B2, C1, C2}
            "grammatic_exceptions": "str",
            "grammatic_exceptions_score": "float",
            "lexical_weaknesses": "str",
            "lexical_weaknesses_score": "float",
            "additional_comments": "str",
            "pragmatic_context": "str",
            "pragmatic_context_score": "float",
            "stylistic_appropriateness": "str",
            "stylistic_appropriateness_score": "float",
            "vocabulary_diversity": "str",
            "vocabulary_diversity_score": "float",
            "sentence_complexity": "str",
            "sentence_complexity_score": "float",
            "engagement_level": "str",
            "engagement_level_score": "float",
            "tone_and_sentiment": "str",
            "tone_and_sentiment_score": "float",
            "overall_score": "float" # Average percentage score of all indicators
        }\n\n"""
        f"Important notes:\n"
        f"1. Ensure all descriptive fields (e.g., grammatic_exceptions, lexical_weaknesses, etc.) are written in {language}.\n"
        f"2. The response must strictly follow the JSON structure above.\n"
        f"3. Send only the JSON format as the output, without any additional text or explanation!"
    )

    data_from_ai = await connect_gpt_client_and_send_message(prompt, GPT_API_KEY)

    language_level_data = json.loads(data_from_ai)

    return language_level_data


async def connect_gpt_client_and_send_message(message: str, GPT_API_KEY: str) -> str:
    client = OpenAI(api_key=GPT_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}],
        max_tokens=3000,
        temperature=0.7,
        n=1,
        stop=None,
    )

    completion = str(response.choices[0].message.content)

    return completion
