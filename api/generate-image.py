from openai import OpenAI
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
import re
import requests
import time
import tempfile

load_dotenv()

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

@app.after_request
def add_security_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response

@app.route('/api/generate-image', methods=['POST'])
def genImage():
    imageSize = request.form.get('imageSize')
    text = request.form.get('text')
    uid = request.form.get('uid')
    index = int(request.form.get('index'))  # Get the index from the request

    temp_dir = tempfile.gettempdir()  # Get the system temporary directory
    
    # Split the text into parts
    parts = re.split(r'Part \d+:', text)
    if parts[0] == '':
        parts.pop(0)
    parts = [part.strip() for part in parts]
    
    if index < 0 or index >= len(parts):
        return jsonify(message='Index out of range'), 400

    image_url = createImage(parts[index], imageSize)
    if image_url:
        img_temp_path = os.path.join(temp_dir, f'image_{index}_{uid}.png')
        download_image(image_url, img_temp_path)
        return send_file(img_temp_path, mimetype='image/png')
    else:
        return jsonify(message='Failed to generate image'), 500

def createImage(textPrompt, imageSize, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=textPrompt,
                size=imageSize,
                quality="standard",
                n=1,
            )
            # Assuming response structure matches your API's design
            return response.data[0].url
        except Exception as e:
            print(f"Error generating image, attempt {attempt+1}: {e}")
            attempt += 1
            if attempt < retries:
                time.sleep(delay)  # Wait before retrying
    return None

def download_image(url, path):
    """Download an image from a URL to a local path."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url}")

if __name__ == '__main__':
    app.run()
