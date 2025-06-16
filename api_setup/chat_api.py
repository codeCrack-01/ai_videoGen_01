### This file will be used to experiment with things!
import os
from dotenv import load_dotenv

from google import genai

def main_func(prompt):
    load_dotenv()
    client = genai.Client(api_key=os.environ['API_KEY'])

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    return response.text
