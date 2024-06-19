from openai import OpenAI
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import re
import requests
import time

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

@app.route('/api/generate-images', methods=['POST', 'GET'])
def genImages():
    imageSize = request.form.get('imageSize')
    text = request.form.get('text')
    uid = request.form.get('uid')
    image_paths = []
    image_urls = []
    
    if 'images' in request.files:
        image_files = request.files.getlist('images')
        for index, image in enumerate(image_files):
            img_temp_path = f'image_{index}_{uid}.png'
            image.save(img_temp_path)
            image_paths.append(img_temp_path)
    
    if not 'images' in request.files:
        if imageSize:
            image_urls = createImages(text, imageSize)
            for index, image_url in enumerate(image_urls):
                img_temp_path = f'image_{index}_{uid}.png'
                download_image(image_url, img_temp_path)
                image_paths.append(img_temp_path)

    if image_urls:
      return jsonify(image_urls=image_urls, image_paths=image_paths), 200
    else:
      return jsonify(message='OK'), 200
    
def createImages(textPrompt, imageSize, retries=3, delay=2):
    images = []
    parts = re.split(r'Part \d+:', textPrompt)

    # Remove the first element if it's empty (which happens if the text starts with "Part 1:")
    if parts[0] == '':
        parts.pop(0)

    # Strip leading and trailing whitespace from each part
    parts = [part.strip() for part in parts]
    print(parts)
    for x in range(len(parts)):
        attempt = 0
        while attempt < retries:
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=parts[x],
                    size=imageSize,
                    quality="standard",
                    n=1,
                )
                # Assuming response structure matches your API's design
                images.append(response.data[0].url)
                break  # Exit the retry loop on success
            except Exception as e:
                print(f"Error generating image for part {x+1}, attempt {attempt+1}: {e}")
                attempt += 1
                if attempt < retries:
                    time.sleep(delay)  # Wait before retrying
    print(images)
    return images


def download_image(url, path):
  """Download an image from a URL to a local path."""
  response = requests.get(url)
  if response.status_code == 200:
    with open(path, 'wb') as file:
      file.write(response.content)
  else:
    print(f"Failed to download {url}")