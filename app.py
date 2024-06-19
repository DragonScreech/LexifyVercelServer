from flask import Flask, jsonify, request
from pdfminer.high_level import extract_text
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

def createScript(prompt, textReplaced):
  if not textReplaced:
    rewrittenPrompt = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[{
        "role": 'user',
        "content": """Rewrite the following prompt in a way that reads 'tell me about ___" rather than make a video about ___

  Ex: Make a video about bees. Split the story into 5 parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes.  -> Tell me about bees. Split the story into 5 parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes.

  Make sure to only change the first sentence. It is crucial that you do not change the other sentences describing the formatting. Also, even if it says to make the script in another lanuage, leave this rewritten prompt in english

  Here is the text: """ + prompt
      }]
    )

    promptText = rewrittenPrompt.choices[0].message.content
    print(promptText)
  else:
    promptText = prompt

  response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[{
         "role": 'system',
         "content": 'You are an ai assisant that users depend on to make video scripts. However, when people say to make a video, just ignore that and move on like they just asked you to tell them about something. DO NOT include any headings and leave the entire thing as plain text.'
      }, {
          "role": 'user',
          "content": promptText
      },],
      max_tokens=100,
  )
  print(response.choices[0].message.content)
  return response.choices[0].message.content

@app.route('/', methods=['POST', 'GET'])
def hello():
    some_param = request.form.get('param')
    return jsonify(param="here is the param" + some_param)

@app.route('/generate-script', methods=['POST', 'GET'])
def genScript():
    if 'prompt' not in request.form:
        return jsonify({"error": "Prompt is required"}), 400

    # Extract prompt and (optional) script text
    prompt_text = request.form['prompt']
    language  = request.form.get('language')
    strNumImages = request.form['imageCount']
    numImages = int(strNumImages)
    script_text = request.form.get('script')
    uid = request.form.get('uid')

    if 'pdf' in request.files:
      pdf_file = request.files['pdf']
      pdf_file.save(f'user_pdf_{uid}.pdf')
      pdfText = extract_text(f'user_pdf_{uid}.pdf')
      print(pdfText)

    if script_text:
        generated_text = createScript(script_text + f" Split the story into {numImages} parts like so: Part 1: text  Part 2: text and so on. Do NOT change anything else about the text at ALL. DO NOT make the part markers in headings just leave them as plain text", True)
    else:
        if language:
           language_text = f'Make the script in {language}. However, make sure to leave the Part markers in english'
        else:
           language_text = ''
        if 'pdf' in request.files:
            generated_text = createScript(prompt_text + f"Split the story into {numImages} parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes. {language_text} Also, make sure to use this information: {pdfText}", False)
        else: 
            generated_text = createScript(prompt_text + f"Split the story into {numImages} parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes. {language_text}", False)

    time.sleep(16)

    return generated_text

if __name__ == "__main__":
    app.run()

