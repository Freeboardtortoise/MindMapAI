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
I would like you do the following for each note:
- come up with ideas based on the notes and the contents of the notes in the JSON input
- come up with an importance factor for each idea
- give me ideal x and y coordenates for each node so that if plotted... looks natural and doesn't overlap and is relitivly spaced out
- give me ideal width and hight for each node
- give me a list of titles to other ideas that are potentialy related to the current note
- give me a hex code for the color of the note and the color of the text to make sure it stands out the apropriat amount
 
add as many as you deem nececery to transfur the meening across clearly

please don't use the direct titles of the notes but rather topics/titles that coresspond to the ideas that you come up with

please make sure the text is easely identafyable on the block of "color"

make sure the connections are the same name as the nodes name

example:

{
    "idea1": {
        "connections": ["note2", "note3"],
        "color": "#ff0000",
        "text-color":"#55ff55",
        "importance": 1,
        "x":100,
        "y":20,
        "width":100,
        "hight":45
    },
    "idea2": {
        "connections": ["note1", "note3"],
        "color": "#ff0011",
        "text-color":"#55fee44",
        "importance": 0.45,
        "x":320,
        "y":134,
        "width":87,
        "hight":84
    },
    "concept2": {
        "connections": ["note1", "note3"],
        "color": "#ff0044",
        "text-color":"#f056006"
        "importance": 0.65,
        "x":34,
        "y":67,
        "width":455,
        "hight":98
    },
    "idea3": {
        "connections": ["note1", "note2"],
        "color": "#f405600",
        "text-color" "#f56650",
        "importance": 0.94,
        "x":56,
        "y":26,
        "width":67
        "height"678
    }
}

Return only valid JSON — no explanation, no preamble.
please make sure the connections and names are constant and don't differ from other nodes connections


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
    answere = ask_question(""" you will be given a json input and I would like you to make me an order of the nodes in the map and x and y cords and sizes regarding the percieved importance or the node as well as colors for the importtance of the node witch will be provided in the input
                           i would like them reliivly spaces out
                           your input is in the for of json
                           
                           Return only valid JSON — no explanation, no preamble.
                           DO NOT ADD ANY EXTRA ONES
                           here is an example of what I would like you to give me:
                           
                           {"note name": {"x": 10, "y": 1000, "width": 40, "height": 40, "color": "#ff0000"}, {"other note name": {"x": 10, "y": 10, "width": 50, "height": 50, "color": "#00ff00"}}}
                           width and height are in pixels (please make sure all of the nodes look natural and stay within the screen): and order
                           width: """ + str(width) + """
                           height: """ + str(height) + """

                           I would like it to look natural
                           Input in json format:
                           """ + repr(mindmap))
    
    print(f"answere: {answere}")
    return extract_json(answere)
