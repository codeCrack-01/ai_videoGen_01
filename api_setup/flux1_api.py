import os
from dotenv import load_dotenv

from gradio_client import Client

load_dotenv()
hf_token = os.environ['HF_TOKEN']

def gen_image(prompt):
    try:
        client = Client("black-forest-labs/FLUX.1-schnell", hf_token=hf_token)
    except Exception as e:
        return e.__traceback__

    result = client.predict(
    	prompt=prompt,
    	seed=0,
    	randomize_seed=True,
    	width=1920,
    	height=1080,
    	num_inference_steps=4,
    	api_name="/infer"
    )

    return result
