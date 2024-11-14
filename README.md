# AI Education Assistant

## Project Overview:
This project focuses on developing an AI-powered educational tool that enhances learning by providing both dynamic, contextually relevant text explanations and corresponding visual content for every paragraph.
## Goal:
To make complex concepts easier to understand by combining detailed explanations with suitable images, creating a more engaging and interactive learning experience.

## Features
 1. Improves Comprehension:Visual aids help students understand and retain information better, especially for abstract subjects.
 2. Provides Contextual Learning:Images help students connect theoretical knowledge with real-world examples.
 3. Supports Different Learning Styles:The tool accommodates both visual and text-based learners.
 4. Increases Engagement & Motivation:By gamifying learning, the tool keeps students engaged for longer periods.


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

1. Run the main script and enter a story prompt:
   ```bash
   python app.py

2. The script will:
   Generates a multi-part story, each part accompanied by a prompt for an image.
   Fetch and display each generated image along with its associated story part.
   Compile the images and text into a downloadable PDF.


## Configuration Details

**Generative Model Configuration:** Uses parameters like temperature, top_p, and top_k to customize the generated output.
**Safety Settings:** Configured to filter content for appropriate outputs.
**PDF Generation:** Utilizes reportlab to format and style the PDF with images and text positioned accurately for a polished result.

## Dependencies
google.generativeai
reportlab
requests
Pillow
opencv-python
textwrap

## Example Output

## The generated PDF includes:

![image](https://github.com/user-attachments/assets/8cd4a543-3013-4a69-b0f9-6023a3bcf73f)

![image](https://github.com/user-attachments/assets/92e70d4c-94bd-4cd6-8762-d28d508860db)

![image](https://github.com/user-attachments/assets/8b745e0b-e1e5-4929-87be-d8c808967972)


Enjoy exploring AI-powered Education Assitant with this project!

