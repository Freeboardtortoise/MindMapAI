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
I would like you to come up with ideas based on the notes and the content in the JSON input.
I would not like you to use the notes directly in the output. but rather ideas related to the notes for example:
for an input of notes about neurons use nodes about things in the notes content that will be relevant to neurons.
place a short sumery under "sumery": the color of the connection 'in hex code' and connections in a list with only the titles of the ideas under "connections":
add as many as you deem nececery

example:

{
    "idea1": {
        "sumery": "short sumery",
        "connections": ["note2", "note3"],
        "color": "#ff0000"
    },
    "idea2": {
        "sumery": "short sumery",
        "connections": ["note1", "note3"],
        "color": "#ff0011"
    },
    "concept2": {
        "sumery": "short sumery",
        "connections": ["note1", "note3"],
        "color": "#ff0044"
    },
    "idea3": {
        "sumery": "short sumery",
        "connections": ["note1", "note2"],
        "color": "#f405600"
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