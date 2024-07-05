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

@app.route('/questions', methods = ['POST', 'GET'])
def Server_Questions():
    transcript = request.form.get('transcript')
    return createQuestions(transcript)

def createQuestions(prompt):
  response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[{
         "role": 'system',
         "content": """You are an ai assisant that makes a list of questions pertaining to the text the user gives you. Format them like this. 
         Q1: Question
         A: answer
         B: answer - correct
         C: answer
         D: answer
         Q2: Question
         and so on"""
      }, {
          "role": 'user',
          "content": prompt
      },],
      max_tokens=500,
  )
  print(response.choices[0].message.content)
  return(response.choices[0].message.content)