# AI Story Generator

## Project Overview

This project demonstrates the use of Google’s Generative AI, specifically the `gemini-1.5-flash` model, to create interactive, image-rich stories from user-provided prompts. By generating narrative text along with image prompts, the project transforms storytelling into a visual and engaging experience, packaging everything into a downloadable PDF.

## Features

- **AI-Generated Stories**: Takes a user prompt and creates a complete storyline, with detailed scene descriptions.
- **AI-Powered Image Generation**: Each scene includes a prompt to generate an image that visually represents the story's setting or action.
- **PDF Output**: Compiles the story text and images into a well-structured PDF, offering users a downloadable keepsake.

## Project Structure

- **`app.py`**: The primary script for interacting with the user, generating the story, fetching images, and compiling the PDF.
- **`api.txt`**: Stores the API key for accessing Google Generative AI.
- **`requirements.txt`**: Lists necessary dependencies such as `google.generativeai`, `reportlab`, `requests`, `Pillow`, and `opencv-python`.

## Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd project_directory


2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt


3. Add your Google Generative AI API key to api.txt.

## Usage

Run the main script and enter a story prompt:
   ```bash
   python app.py



## The script will:

Generates a multi-part story, each part accompanied by a prompt for an image.
Fetch and display each generated image along with its associated story part.
Compile the images and text into a downloadable PDF.
