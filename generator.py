import json
import time
import re

from config import client
from prompt import PROMPT
from utils import clean_json_response
from database.database import (
    get_knowledge,
    insert_knowledge,
    insert_questions
)


def generate_knowledge(topic_info):

    # -------------------------------
    # Check Database First
    # -------------------------------

    knowledge = get_knowledge(topic_info["topic"])

    if knowledge:
        print("✅ Loaded From Database")
        return knowledge

    print(f"🤖 Generating {topic_info['topic']}...")

    # -------------------------------
    # Ask Gemini (API Retry)
    # -------------------------------

    MAX_API_RETRIES = 3

    for attempt in range(MAX_API_RETRIES):

        try:

            retry_prompt = (
                PROMPT
                + topic_info["topic"]
                + """

            IMPORTANT:

            Your previous response contained invalid JSON.

            Return ONLY valid JSON.

            Double-check that:
            - Every array is closed with ]
            - Every object is closed with }
            - Every key/value pair is separated by commas
            - The JSON can be parsed directly using Python json.loads()

            Do not include markdown.
            Do not include explanations.
            Return only one valid JSON object.
            """
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=retry_prompt
            )

            break

        except Exception as e:

            print(f"❌ API Attempt {attempt + 1}/{MAX_API_RETRIES} failed")
            print(e)

            if attempt == MAX_API_RETRIES - 1:
                print(f"⏭ Skipping Topic : {topic_info['topic']}")
                return None

            print("Retrying in 10 seconds...")
            time.sleep(10)

    # -------------------------------
    # Clean Gemini Response
    # -------------------------------

    text = clean_json_response(response.text)

    print("\n" + "=" * 80)
    print("TOPIC:", topic_info["topic"])
    print("=" * 80)
    print(text)
    print("=" * 80 + "\n")

    # -------------------------------
    # JSON Parsing Retry
    # -------------------------------

    MAX_JSON_RETRIES = 3

    for attempt in range(MAX_JSON_RETRIES):

        try:

            data = json.loads(text)
            break

        except json.JSONDecodeError:

            print("\n" + "=" * 80)
            print("❌ Invalid JSON")
            print("Topic:", topic_info["topic"])
            print(f"Retry {attempt + 1}/{MAX_JSON_RETRIES}")
            print("=" * 80)

            if attempt == MAX_JSON_RETRIES - 1:

                print(f"⏭ Skipping Topic : {topic_info['topic']}")
                return None

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=PROMPT + topic_info["topic"]
                )

                text = clean_json_response(response.text)

                print("\n" + "=" * 80)
                print(f"RETRY {attempt + 2}")
                print("TOPIC:", topic_info["topic"])
                print("=" * 80)
                print(text)
                print("=" * 80 + "\n")

            except Exception as e:

                print(e)
                return None

    # -------------------------------
    # Validate Required Fields
    # -------------------------------

    questions = data.get("questions", [])

    if not questions:

        print(f"⏭ No questions generated for {topic_info['topic']}")
        return None

    # -------------------------------
    # Save Knowledge
    # -------------------------------

    knowledge_data = {

        "definition": data.get("definition", ""),

        "concepts": data.get("concepts", []),

        "ideal_answer": data.get("ideal_answer", ""),

        "rubric": data.get("rubric", []),

        "common_mistakes": data.get("common_mistakes", [])

    }

    insert_knowledge(
        topic_info,
        knowledge_data
    )

    saved = get_knowledge(topic_info["topic"])

    insert_questions(
        saved["id"],
        questions
    )

    print("✅ Saved Successfully")

    return saved