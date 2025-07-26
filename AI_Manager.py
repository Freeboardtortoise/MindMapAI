import os
import json
from groq import Groq
import re

def extract_json(text):
    try:
        json_str = re.search(r"\{.*\}", text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        print("Failed to extract JSON:", e)
        return None

client = Groq(api_key="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")


def generate_mindmap(notes: list[str]) -> dict:
    if not notes:
        return {}

    formatted_notes = "\n".join(f"- {note}" for note in notes)

    prompt = f"""
You are a mind mapping assistant.

Given a list of notes or ideas, return a JSON object representing a structured mind map. 
Group related items under categories or themes. If multiple levels of grouping are needed, use nested dictionaries.

Return only valid JSON — no explanation, no preamble.

Input:
{formatted_notes}
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": prompt.strip()}
            ]
        )

        content = response.choices[0].message.content.strip()

        # Cleanly parse the output into a Python dict
        mindmap = extract_json(content)
        return mindmap

    except Exception as e:
        print("❌ Error contacting Groq or parsing response:", e)
        return {}
def ask_question(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": prompt.strip()}
            ]
        )

        content = response.choices[0].message.content.strip()

        # Cleanly parse the output into a Python dict
        print("Raw model response:")
        return content

        mindmap = extract_json(content)
        return mindmap

    except Exception as e:
        print("❌ Error contacting Groq or parsing response:", e)
        return {}