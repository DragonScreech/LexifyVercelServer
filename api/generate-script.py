# from openai import OpenAI
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# CORS(app)
# client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

# @app.route('/api/generate-script', methods=['POST'])
# def generate_script():
#     prompt_text = request.form['prompt']
#     language = request.form.get('language')
#     num_images = int(request.form['imageCount'])
#     script_text = request.form.get('script')
#     uid = request.form.get('uid')

#     if script_text:
#         generated_text = create_script(script_text + f" Split the story into {num_images} parts like so: Part 1: text  Part 2: text and so on. Do NOT change anything else about the text at ALL. DO NOT make the part markers in headings just leave them as plain text", True)
#     else:
#         language_text = f'Make the script in {language}. However, make sure to leave the Part markers in english' if language else ''
#         generated_text = create_script(prompt_text + f"Split the story into {num_images} parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes. {language_text}", False)

#     return generated_text

# def create_script(prompt, text_replaced):
#     if not text_replaced:
#         rewritten_prompt = client.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[{
#                 "role": 'user',
#                 "content": """Rewrite the following prompt in a way that reads 'tell me about ___" rather than make a video about ___

#                 Ex: Make a video about bees. Split the story into 5 parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes.  -> Tell me about bees. Split the story into 5 parts like so: Part 1: text  Part 2: text and so on. DO NOT make the part markers in headings just leave them as plain text. Make sure to keep fairly short. Reading it should take 1 - 2 minutes.

#                 Make sure to only change the first sentence. It is crucial that you do not change the other sentences describing the formatting. Also, even if it says to make the script in another lanuage, leave this rewritten prompt in english

#                 Here is the text: """ + prompt
#             }]
#         )

#         prompt_text = rewritten_prompt.choices[0].message.content
#     else:
#         prompt_text = prompt

#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[{
#             "role": 'system',
#             "content": 'You are an ai assisant that users depend on to make video scripts. However, when people say to make a video, just ignore that and move on like they just asked you to tell them about something. DO NOT include any headings and leave the entire thing as plain text.'
#         }, {
#             "role": 'user',
#             "content": prompt_text
#         }],
#         max_tokens=500,
#     )
#     return response.choices[0].message.content

# if __name__ == '__main__':
#     app.run()
