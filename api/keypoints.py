from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

@app.after_request
def add_security_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response

@app.route('/keypoints', methods = ['POST', 'GET'])
def Server_Keys():
    transcript = request.form.get('transcript')
    return createKeyPoints(transcript)

def createKeyPoints(prompt):
  response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[{
         "role": 'system',
         "content": 'You are an ai assisant that makes a list of keypoints from a text that the user will give you. Make sure to format the keypoints like this: 1. Keypoint 1 2. Keypoint 2 and so on. Leave it all as plain text and dont include any bold or heading text'
      }, {
          "role": 'user',
          "content": prompt
      },],
      max_tokens=500,
  )
  text = response.choices[0].message.content
  lines = text.split('\n')

  # Create a list to store the values
  values = []

  # Process each line individually
  for line in lines:
    # Strip leading and trailing whitespace
    line = line.strip()

    # Find the first space after the number, marking the start of the value
    first_space_index = line.find(" ")
    if first_space_index == -1:
      # If no space is found, skip this line
      continue

    # Extract the value after the first space
    value = line[first_space_index + 1:].strip()

    # Add to the list
    values.append(value)
  
  print(values)
  return values