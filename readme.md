 # ACCENTURE INNOVATION


```python
import json
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import io
import requests
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import textwrap
```


```python
with open('api.txt') as f:
    f = f.read()
```


```python
key = f
```


```python
genai.configure(api_key=key)
```


```python
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}
```


```python
generation_config
```




    {'temperature': 1,
     'top_p': 0.95,
     'top_k': 64,
     'max_output_tokens': 8192,
     'response_mime_type': 'application/json'}




```python
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings= {
  #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
  #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
  #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
  #     HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE
  # },
  system_instruction="You are part of a book generator system. When the user provides a prompt for a story, your task is to create the story along with a detailed prompt for generating an image. The image prompt should appear before each part of the storyline in a key-value format. Additionally, provide a suitable title for the story and structure the response in a clear and organized forma",
)
```


```python
model
```




    genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        generation_config={'temperature': 1, 'top_p': 0.95, 'top_k': 64, 'max_output_tokens': 8192, 'response_mime_type': 'application/json'},
        safety_settings={},
        tools=None,
        system_instruction='You are part of a book generator system. When the user provides a prompt for a story, your task is to create the story along with a detailed prompt for generating an image. The image prompt should appear before each part of the storyline in a key-value format. Additionally, provide a suitable title for the story and structure the response in a clear and organized forma',
    )




```python
chat_session = model.start_chat(
  history=[]
)
```


```python
chat_session
```




    ChatSession(
        model=genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            generation_config={'temperature': 1, 'top_p': 0.95, 'top_k': 64, 'max_output_tokens': 8192, 'response_mime_type': 'application/json'},
            safety_settings={},
            tools=None,
            system_instruction='You are part of a book generator system. When the user provides a prompt for a story, your task is to create the story along with a detailed prompt for generating an image. The image prompt should appear before each part of the storyline in a key-value format. Additionally, provide a suitable title for the story and structure the response in a clear and organized forma',
        ),
        history=[]
    )




```python
def gen_im(prompt,file_name):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": "Bearer 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"}
    payload={"inputs": f"{prompt}",}
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    image.save(f"/content/{file_name}.png","PNG")
    return f"/content/{file_name}.png"
```


```python
prompt=input("Enter Your prompt: ")
response = chat_session.send_message(f"{prompt}")
```

    Enter Your prompt: A Ghost Story
    


```python
response
```




    response:
    GenerateContentResponse(
        done=True,
        iterator=None,
        result=glm.GenerateContentResponse({'candidates': [{'content': {'parts': [{'text': '{"title": "The Whispering Attic", "story": [{"image_prompt": "A dusty old attic with cobwebs hanging from the rafters, a single ray of sunlight illuminating a worn wooden chest in the corner", "story_part": "The old house creaked and groaned, its timbers settling with the passing years. Amelia, a young woman with eyes as bright as the summer sky, stood on the threshold of the attic, a chill wind whistling through the cracks in the roof. Her grandmother, a woman with stories etched in her wrinkles, had left Amelia the house, a legacy of memories and secrets. Amelia had always been fascinated by the attic, its air thick with the scent of dust and forgotten dreams."}, {"image_prompt": "Amelia opening a wooden chest, revealing old photographs and dusty letters inside, her face a mixture of curiosity and apprehension", "story_part": "The attic was a labyrinth of forgotten treasures. A chipped porcelain doll stared blankly from a dusty shelf, and a worn leather-bound journal lay open on a table, its pages filled with faded ink. Amelia\'s fingers traced the edges of a wooden chest, its hinges creaking as she lifted the lid. Inside, she found a collection of faded photographs and yellowed letters, their contents whispering tales of a past she had never known."}, {"image_prompt": "A spectral figure in a white gown, translucent and ethereal, standing in the attic, its eyes glowing with an eerie blue light", "story_part": "As she sifted through the memories, a cold shiver ran down Amelia\'s spine. The air grew heavy, and the scent of lavender, her grandmother\'s favorite, filled the room. She felt a presence, a whisper against her skin, a feeling of being watched. Turning slowly, she saw her, a figure in a white gown, translucent and ethereal, her eyes glowing with an eerie blue light. The ghost of her grandmother stood before her, a silent guardian of the past."}, {"image_prompt": "Amelia and the ghost of her grandmother, hand in hand, looking out of the attic window at a beautiful sunset over a rolling countryside", "story_part": "Amelia, trembling with a mixture of fear and awe, reached out a hand. The ghost, with a gentle smile, took her hand in hers, a cold touch that felt strangely comforting. As the sun dipped below the horizon, casting long shadows across the attic floor, Amelia realized that the whispers she had heard weren\'t meant to frighten her, but to guide her. The attic, once a place of forgotten memories, had become a bridge between her and the past, a testament to the enduring power of family and love."}], "end": "Amelia, the ghost of her grandmother by her side, looked out of the attic window, the setting sun painting the sky in shades of orange and purple. The past and present intertwined, their whispers echoing through the old house, a symphony of love and loss, a reminder that even in the shadows, there is always light."}\n'}], 'role': 'model'}, 'finish_reason': 1, 'index': 0, 'safety_ratings': [{'category': 9, 'probability': 1, 'blocked': False}, {'category': 8, 'probability': 1, 'blocked': False}, {'category': 7, 'probability': 1, 'blocked': False}, {'category': 10, 'probability': 1, 'blocked': False}], 'token_count': 0, 'grounding_attributions': []}]}),
    )




```python
answer=json.loads(response.text)
```


```python
answer
```




    {'title': 'The Whispering Attic',
     'story': [{'image_prompt': 'A dusty old attic with cobwebs hanging from the rafters, a single ray of sunlight illuminating a worn wooden chest in the corner',
       'story_part': 'The old house creaked and groaned, its timbers settling with the passing years. Amelia, a young woman with eyes as bright as the summer sky, stood on the threshold of the attic, a chill wind whistling through the cracks in the roof. Her grandmother, a woman with stories etched in her wrinkles, had left Amelia the house, a legacy of memories and secrets. Amelia had always been fascinated by the attic, its air thick with the scent of dust and forgotten dreams.'},
      {'image_prompt': 'Amelia opening a wooden chest, revealing old photographs and dusty letters inside, her face a mixture of curiosity and apprehension',
       'story_part': "The attic was a labyrinth of forgotten treasures. A chipped porcelain doll stared blankly from a dusty shelf, and a worn leather-bound journal lay open on a table, its pages filled with faded ink. Amelia's fingers traced the edges of a wooden chest, its hinges creaking as she lifted the lid. Inside, she found a collection of faded photographs and yellowed letters, their contents whispering tales of a past she had never known."},
      {'image_prompt': 'A spectral figure in a white gown, translucent and ethereal, standing in the attic, its eyes glowing with an eerie blue light',
       'story_part': "As she sifted through the memories, a cold shiver ran down Amelia's spine. The air grew heavy, and the scent of lavender, her grandmother's favorite, filled the room. She felt a presence, a whisper against her skin, a feeling of being watched. Turning slowly, she saw her, a figure in a white gown, translucent and ethereal, her eyes glowing with an eerie blue light. The ghost of her grandmother stood before her, a silent guardian of the past."},
      {'image_prompt': 'Amelia and the ghost of her grandmother, hand in hand, looking out of the attic window at a beautiful sunset over a rolling countryside',
       'story_part': "Amelia, trembling with a mixture of fear and awe, reached out a hand. The ghost, with a gentle smile, took her hand in hers, a cold touch that felt strangely comforting. As the sun dipped below the horizon, casting long shadows across the attic floor, Amelia realized that the whispers she had heard weren't meant to frighten her, but to guide her. The attic, once a place of forgotten memories, had become a bridge between her and the past, a testament to the enduring power of family and love."}],
     'end': 'Amelia, the ghost of her grandmother by her side, looked out of the attic window, the setting sun painting the sky in shades of orange and purple. The past and present intertwined, their whispers echoing through the old house, a symphony of love and loss, a reminder that even in the shadows, there is always light.'}




```python
image_prompt=[]
Story=[]

for item in answer['story']:
  image_prompt.append(item['image_prompt'])
  Story.append(item["story_part"])
```


```python
images=[]
for i,image in enumerate(image_prompt):
  images.append(gen_im(image,f"image{i+1}"))

for i in range(len(images)):
    image = images[i]
    st = Story[i]
    im = cv2.imread(image)
    im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    plt.imshow(im_rgb)
    plt.axis('off')
    plt.show()

    print(st)
    print()
```


    
![png](output_17_0.png)
    


    The old house creaked and groaned, its timbers settling with the passing years. Amelia, a young woman with eyes as bright as the summer sky, stood on the threshold of the attic, a chill wind whistling through the cracks in the roof. Her grandmother, a woman with stories etched in her wrinkles, had left Amelia the house, a legacy of memories and secrets. Amelia had always been fascinated by the attic, its air thick with the scent of dust and forgotten dreams.
    
    


    
![png](output_17_2.png)
    


    The attic was a labyrinth of forgotten treasures. A chipped porcelain doll stared blankly from a dusty shelf, and a worn leather-bound journal lay open on a table, its pages filled with faded ink. Amelia's fingers traced the edges of a wooden chest, its hinges creaking as she lifted the lid. Inside, she found a collection of faded photographs and yellowed letters, their contents whispering tales of a past she had never known.
    
    


    
![png](output_17_4.png)
    


    As she sifted through the memories, a cold shiver ran down Amelia's spine. The air grew heavy, and the scent of lavender, her grandmother's favorite, filled the room. She felt a presence, a whisper against her skin, a feeling of being watched. Turning slowly, she saw her, a figure in a white gown, translucent and ethereal, her eyes glowing with an eerie blue light. The ghost of her grandmother stood before her, a silent guardian of the past.
    
    


    
![png](output_17_6.png)
    


    Amelia, trembling with a mixture of fear and awe, reached out a hand. The ghost, with a gentle smile, took her hand in hers, a cold touch that felt strangely comforting. As the sun dipped below the horizon, casting long shadows across the attic floor, Amelia realized that the whispers she had heard weren't meant to frighten her, but to guide her. The attic, once a place of forgotten memories, had become a bridge between her and the past, a testament to the enduring power of family and love.
    
    


```python
images
```




    ['/content/image1.png',
     '/content/image2.png',
     '/content/image3.png',
     '/content/image4.png']



# Pdf Download


```python
def create_pdf(images, stories, title, output_pdf='output.pdf'):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter  
    c.setFont("Helvetica-Bold", 24)  
    c.drawCentredString(width / 2.0, height - 100, title) 

    for i in range(len(images)):
        image_path = images[i]
        story = stories[i]
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img_rgb)  
        temp_image_path = f"temp_image_{i}.png"  
        im_pil.save(temp_image_path, "PNG")
        image_y_position = 300
        c.drawImage(temp_image_path, x=100, y=image_y_position, width=400, height=300)
        text_y_position = image_y_position - 30  
        c.setFont("Helvetica", 12)  
        max_width = 400  
        wrapped_story = textwrap.wrap(story, width=80)  
        for line in wrapped_story:
            c.drawString(100, text_y_position, line)
            text_y_position -= 15 
        if i < len(images) - 1:
            c.showPage() 
        os.remove(temp_image_path)

    c.save()
```


```python
title = answer['title']
create_pdf(images, Story, title)
print("PDF created Successfully")
```

    PDF created Successfully
    


```python
wrapped_story = textwrap.wrap(Story[0], width=80)
wrapped_story
```




    ['The old house creaked and groaned, its timbers settling with the passing years.',
     'Amelia, a young woman with eyes as bright as the summer sky, stood on the',
     'threshold of the attic, a chill wind whistling through the cracks in the roof.',
     'Her grandmother, a woman with stories etched in her wrinkles, had left Amelia',
     'the house, a legacy of memories and secrets. Amelia had always been fascinated',
     'by the attic, its air thick with the scent of dust and forgotten dreams.']



# END
