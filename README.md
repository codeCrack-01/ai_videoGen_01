# Auto_VIDE0

This project is a bare minimum setup designed to demonstrate a basic application structure. Its primary function is to serve as a foundational template, and it requires specific environment variables to operate correctly.

## Project Overview

This application streamlines the process of generating images from a user-provided script. The general workflow is as follows:

1.  **Script Input**: The user provides a textual script or narrative.
2.  **Visual Prompt Generation**: The application intelligently processes the input script to create detailed visual prompts. This likely involves leveraging the Gemini AI service (indicated by `GEMINI_KEY`) to interpret the script and generate descriptive text suitable for image generation models.
3.  **Image Generation**: The generated visual prompts are then used to create images. This project utilizes the Flux1 model via the Hugging Face API (indicated by `HF_TOKEN`) to generate these images based on the refined prompts.


## Getting Started

To run this project, you need to set up your environment variables. Create a file named `.env` in the root directory of the project.

### Environment Variables

The following keys **must** be provided in your `.env` file:

- `SECRET_KEY`: A unique and strong secret key for application security (e.g., Flask applications).
- `GEMINI_KEY`: Your API key for accessing the Gemini AI service.
- `HF_TOKEN`: Your authentication token for Hugging Face services.
- `TEST_IPROMPT`: A default input prompt used for testing purposes within the application.
- `FLASK_APP`: Specifies the Flask application entry point (e.g., `my_app.app:create_app`).

Example `.env` file:
```/dev/null/example.env#L1-5
SECRET_KEY="your_super_secret_key_here"
GEMINI_KEY="your_gemini_api_key_here"
HF_TOKEN="your_huggingface_token_here"
TEST_IPROMPT="Your default test prompt text."
FLASK_APP=my_app.app:create_app
```

Once your `.env` file is configured, you can proceed with installing dependencies and running the application as per standard Python/Flask project setup.