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

@app.route('/flashcards', methods = ['POST', 'GET'])
def Server_FlashCards():
    transcript = request.form.get('transcript')
    return createFlashcards(transcript)

def createFlashcards(prompt):
  response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
       "role": 'system',
       "content": """You are an ai assistant that makes different informational flashcards relating to the prompt the user has given. You will format the flashcards like this:
       Flashcard 1
       Front of card: Question about topic
       Back of card: Answer

       Flashcard 2
        Front of card: Question about topic
        Back of card: Answer

      Flashcard 3
       Front of card: Question about topic
       Back of card: Answer

      Flashcard 4
       Front of card: Question about topic
       Back of card: Answer

      Flashcard 5
       Front of card: Question about topic
       Back of card: Answer
       """    
      }, {
        "role": 'user',
        "content": prompt
      },],
      max_tokens=500,
)

  print(response.choices[0].message.content)
  return(response.choices[0].message.content)