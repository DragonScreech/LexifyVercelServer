from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import os
import re
import tempfile
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

@app.route('/api/generate-audio', methods=['POST'])
def genAudio():
    uid = request.form['uid']
    text = request.form['text']
    audio_path = os.path.join('/tmp', f'speech_{uid}.mp3')
    createAudio(text, uid, audio_path)
    return send_file(audio_path, as_attachment=True, download_name='speech.mp3')

def createAudio(text, uid, audio_path):
    cleaned_text = re.sub(r'Part \d+:', '', text)
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=cleaned_text)
    response.stream_to_file(audio_path)

if __name__ == '__main__':
    app.run()
