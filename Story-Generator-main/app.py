from flask import Flask, render_template, request, jsonify
import json
import google.generativeai as genai
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image as PILImage  # Rename PIL's Image
import io
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as ReportLabImage  # Rename ReportLab's Image
import os

app = Flask(__name__)

genai.configure(api_key="AIzaSyAtPsFi6PlM3Yh8AHabXjoApCPsHVkyv_E")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

history = []
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL': 'BLOCK_NONE',
        'DANGEROUS': 'BLOCK_NONE'
    },
    system_instruction="""
    You are part of a book generator system. When the user provides a prompt for a story or requests modifications, your task is to:
    1. Create or modify the story in a clear, structured format with multiple sections, each containing rich, detailed content.
    2. Ensure each section has at least 10-13 sentences, is well-structured, and cohesive.
    3. Output format should be JSON with a "title" and "story" array of { "image_prompt": "...", "story_part": "..." } objects.
    """
)

def gen_im(prompt, file_name, retries=3, initial_delay=20, backoff_factor=3):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": f"{prompt}"}

    delay = initial_delay
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            image_bytes = response.content
            image = PILImage.open(io.BytesIO(image_bytes))
            image.save(f"static/image/{file_name}.png", "PNG")
            return f"static/image/{file_name}.png"
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Too many requests
                print(f"Rate limit reached, retrying after {delay} seconds...")
                time.sleep(delay)
                delay *= backoff_factor  # Exponential backoff
            else:
                print(f"Error generating image (attempt {attempt + 1}/{retries}): {e}")
                return "static/images/placeholder.png"
        except requests.exceptions.RequestException as e:
            print(f"Error generating image (attempt {attempt + 1}/{retries}): {e}")
            return "static/images/placeholder.png"

def generate_story(prompt, retries=3, delay=2):
    for attempt in range(retries):
        try:
            chat_session = model.start_chat(history=history)
            response = chat_session.send_message(f"{prompt}")
            answer_text = response.text

            try:
                answer = json.loads(answer_text)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response text: {answer_text[:500]}...")  # Log part of the response for inspection
                return None  # Skip this attempt if JSON is invalid

            history.append({"role": "user", "parts": [prompt]})
            history.append({"role": "model", "parts": [json.dumps(answer)]})
            return answer
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Error generating text (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Add delay between retries
            else:
                return None

def generate_images_concurrently(image_prompts):
    images = []
    with ThreadPoolExecutor(max_workers=1) as executor:  # Use only 1 worker to avoid overloading the API
        futures = {executor.submit(gen_im, prompt, f"image{i+1}"): i for i, prompt in enumerate(image_prompts)}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                image_path = future.result()
                if image_path:
                    images.append((idx, image_path))
                else:
                    print(f"Image generation failed for prompt {idx + 1}")
                    images.append((idx, "static/images/placeholder.png"))
            except Exception as e:
                print(f"Error in thread {idx}: {e}")
                images.append((idx, "static/images/placeholder.png"))
            time.sleep(2)  # Add a small delay between requests
    return [image_path for _, image_path in sorted(images)]

@app.route('/')
def index():
    return render_template('Story.html')

@app.route('/generate_story', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')
    
    answer = generate_story(prompt)
    
    if not answer:
        return jsonify({"error": "Story generation failed"})
    
    if "message" in answer:
        return jsonify({"message": answer['message']})

    if 'story' in answer:
        title = answer.get("title", "Untitled Story")
        image_prompts = [item['image_prompt'] for item in answer['story']]
        story_parts = [item["story_part"] for item in answer['story']]
        
        images = generate_images_concurrently(image_prompts)
        
        result = [{"title": title}]
        for i in range(len(story_parts)):
            image_path = images[i] if i < len(images) else None  # Handle missing images gracefully
            result.append({"image": image_path, "story_part": story_parts[i]})
        
        return jsonify(result)
    
    return jsonify({"error": "Unexpected response format"})

if __name__ == "__main__":
    app.run(debug=False)
