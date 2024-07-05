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

@app.route('/api/definitions', methods = ['POST', 'GET'])
def Server_Def():
    transcript = request.form.get('transcript')
    return createDefinitions(transcript)

def createDefinitions(prompt):
  response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[{
         "role": 'system',
         "content": 'You are an ai assisant that makes a list of vocab words and their definitions using the text the user will provide. Format it like this: 1. Vocab word - Definition 2. Vocab word - Definition and so on. Leave it all as plain text and dont include any bold or heading text'
      }, {
          "role": 'user',
          "content": prompt
      },],
      max_tokens=500,
  )
  text = response.choices[0].message.content
  word_def_dict = {}

    # Split the input text into lines
  lines = text.split('\n')

    # Process each line individually
  for line in lines:
    # Strip leading and trailing whitespace
    line = line.strip()

    # Find the first occurrence of " - " which separates word and definition
    split_index = line.find(" - ")
    if split_index == -1:
      # If no " - " is found, skip this line
      continue

    # Extract the word and definition
    word = line[line.find(" ") + 1:split_index].strip()
    definition = line[split_index + 3:].strip()

    # Add to the dictionary
    word_def_dict[word] = definition

  print(word_def_dict)
  return word_def_dict