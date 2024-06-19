from flask import Flask, request, jsonify
from openai import OpenAI
import os
import re
import tempfile
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

@app.route('/api/generate-audio', methods=['POST'])
def genAudio():
    uid = request.form['uid']
    text = request.form['text']
    audio_path = os.path.join('/tmp', f'speech_{uid}.mp3')
    createAudio(text, uid, audio_path)
    return jsonify({"message": "Audio generated", "audio_path": audio_path}), 200

def createAudio(text, uid, audio_path):
    cleaned_text = re.sub(r'Part \d+:', '', text)
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=cleaned_text)
    response.stream_to_file(audio_path)

if __name__ == '__main__':
    app.run()
