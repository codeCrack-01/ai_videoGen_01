from gradio_client import Client #type: ignore

def gen_image():
    client = Client("black-forest-labs/FLUX.1-schnell")

    result = client.predict(
    	prompt="Hello!!",
    	seed=0,
    	randomize_seed=True,
    	width=1920,
    	height=1080,
    	num_inference_steps=4,
    	api_name="/infer"
    )

    return result
