### This file will be used to experiment with things!
import os
from dotenv import load_dotenv
import re
from google import genai

def main_func(prompt):
    load_dotenv()
    client = genai.Client(api_key=os.environ['GEMINI_KEY'])

    full_prompt = (
        f"You are an AI visual prompt writer. Your sole purpose is to generate detailed, descriptive visual prompts "
        f"for an image generation AI, based on the provided script."
        f"Strictly adhere to the specified output format and include no conversational filler, greetings, "
        f"introductions, or conclusions whatsoever. Your output should be ready for direct copy-pasting.\n\n"
        f"**Script:**\n{prompt}\n\n"
        f"**Generate, for each line, highly detailed visual prompts, at least 10, each describing all visual elements from the script.**\n"
        f"**Output Format:**\n"
        f"Prompt1: [Your highly detailed visual prompt for section 1 of the script]\n"
        f"Prompt2: [Your highly detailed visual prompt for section 2 of the script]\n"
        f"Prompt3: [Your highly detailed visual prompt for section 3 of the script]\n"
        f"..."
        f"PromptN: [Your highly detailed visual prompt for section N of the script]"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=full_prompt
    )
    result = remove_formatting(response.text)

    regex_pattern = r"Prompt\d+: (?:.|\n)*?(?=Prompt\d+:|$)"
    matches = re.findall(regex_pattern, result)

    # Print each extracted prompt
    # for i, match in enumerate(matches):
    #     print(f"--- Extracted Prompt {i+1} --- : " + matches[i].strip())

    return (result, matches)


def remove_formatting(text):
    text = text.replace("*", "")
    text = text.replace("~", "")
    text = text.replace("`", "")
    return text
