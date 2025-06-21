import os
import re # For regular expressions to parse numbers from prompt
from typing import Optional # For optional function arguments
from PIL import Image
import hashlib # For creating a unique hash for filenames
from dotenv import load_dotenv

from gradio_client import Client
from huggingface_hub import InferenceClient

load_dotenv()
hf_token = os.environ['HF_TOKEN']

def gen_image_default(prompt):
    client = Client("black-forest-labs/FLUX.1-schnell", hf_token=hf_token)

    result = client.predict(
    	prompt=prompt,
    	seed=0,
    	randomize_seed=True,
    	width=1920,
    	height=1080,
    	num_inference_steps=4,
    	api_name="/infer"
    )
    return result[0]

def gen_image_direct_to_folder(
    prompt: str,
    save_directory: str, # Your target 'static' or other folder
    image_identifier: Optional[str] = None, # Optional identifier for filename
    width: int = 1024,
    height: int = 1024,
    seed: int = 0
) -> str:
    client = InferenceClient(model="black-forest-labs/FLUX.1-schnell", token=hf_token)

    # Ensure the target save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True) # Create if not exists, do not error if already exists

    # Determine the filename identifier
    identifier_for_filename = ""
    if image_identifier is not None:
        # Sanitize the explicit identifier for use in a filename
        identifier_for_filename = str(image_identifier).replace(" ", "_").replace("/", "_").replace("\\", "_")
    else:
        # Attempt to extract a number/identifier from the prompt (e.g., "(1)")
        match = re.search(r'\(([^)]+)\)', prompt)
        if match:
            # Use the captured group as the identifier, sanitize it
            identifier_for_filename = match.group(1).replace(" ", "_").replace("/", "_").replace("\\", "_")
        else:
            # Fallback to a hash of the prompt if no explicit identifier or parsable number in prompt
            identifier_for_filename = hashlib.md5(prompt.encode()).hexdigest()[:8]

    # Clean up part of the prompt for a descriptive filename
    sanitized_prompt_part = "".join(c for c in prompt if c.isalnum() or c.isspace())[:30].strip().replace(" ", "_")
    if not sanitized_prompt_part:
        sanitized_prompt_part = "generated"

    try:
        # Call the text_to_image method. This is expected to return a PIL Image object.
        print(f"Sending prompt to model via InferenceClient: '{prompt}'")
        image_obj = client.text_to_image(
            prompt=prompt,
            seed=seed,
            width=width,
            height=height,
            num_inference_steps=4,
            # Note: No `api_name` parameter for InferenceClient as it's for direct API calls
        )

        if isinstance(image_obj, Image.Image):
            # Construct the final filename in the target directory
            # Assuming PNG output, you can change extension if the model suggests otherwise
            final_filename = f"flux_{sanitized_prompt_part}_{identifier_for_filename}.png"
            final_image_path = os.path.join(save_directory, final_filename)

            # Save the PIL Image object directly to your specified permanent directory
            image_obj.save(final_image_path)
            print(f"Image successfully generated and saved to: {final_image_path}")
            return final_image_path
        else:
            print(f"Unexpected result format from client.text_to_image: {type(image_obj)}")
            raise TypeError("InferenceClient did not return a PIL Image object as expected.")

    except Exception as e:
        print(f"An error occurred during image generation or saving: {e}")
        raise # Re-raise the exception after printing for better error visibility
