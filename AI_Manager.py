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


def generate_mindmap(notes) -> dict:
    if not notes:
        return {}

    formatted_notes = repr(notes)

    prompt = """
You are a mind mapping assistant.

Given a list of notes or ideas, return a JSON object representing a structured mind map. 
for each item in the input place make a profile where you: place a short sumery under "sumery":, a long description under "description": and connections in a list with only the titles of the notes under "connections":
DO NOT ADD ANY EXTA ONES please

example:

{
    "note1": {
        "sumery": "short sumery",
        "description": "long description",
        "connections": ["note2", "note3"]
    },
    "note2": {
        "sumery": "short sumery",
        "description": "long description",
        "connections": ["note1", "note3"]
    },
    "note3": {
        "sumery": "short sumery",
        "description": "long description",
        "connections": ["note1", "note2"]
    }
}

Return only valid JSON — no explanation, no preamble.


Input in json format:
    """ + formatted_notes

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

def generate_node_stuff(mindmap, width, height):
    answere = ask_question(""" you will be given a json input and I would like you to make me an order of the nodes in the map and x and y cords and sizes regarding the percieved importance or the node
                           i would like them reliivly spaces out
                           your input is in the for of json
                           
                           Return only valid JSON — no explanation, no preamble.
                           DO NOT ADD ANY EXTRA ONES
                           here is an example of what I would like you to give me:
                           
                           {"note name": {"x": 10, "y": 1000, "width": 40, "height": 40}, {"other note name": {"x": 10, "y": 10, "width": 50, "height": 50}}}
                           width and height are in pixels:
                           width: """ + str(width) + """
                           height: """ + str(height) + """

                           I would like it to look natural
                           Input in json format:
                           """ + repr(mindmap))
    
    print(f"answere: {answere}")
    return extract_json(answere)