from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from moviepy.editor import ImageSequenceClip
import os
import tempfile
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-video-no-subtitles', methods=['POST'])
def genVideoNoSubtitles():
    uid = request.form['uid']
    duration = int(request.form['duration'])
    strNumImages = request.form['imageCount']
    numImages = int(strNumImages)
    
    # Get the image URLs from the request
    image_urls = [request.form[f'image_url_{index}'] for index in range(numImages)]
    
    # Paths for temporary storage
    temp_dir = tempfile.gettempdir()
    image_paths = [os.path.join(temp_dir, f'image_{index}_{uid}.png') for index in range(numImages)]
    print(image_paths)
    
    # Download the images from the URLs
    for index in range(numImages):
        image_url = image_urls[index]
        image_path = image_paths[index]
        download_image(image_url, image_path)
        print(f'image {index} downloaded!')
    
    # Create video without audio
    temp_video_path = os.path.join(temp_dir, f'final_video_{uid}.mov')
    print(temp_video_path)
    create_video_without_audio(image_paths, numImages, duration, temp_video_path)
    
    return send_file(temp_video_path, as_attachment=True, download_name='final_video.mov')

def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download image from {url}")

def create_video_without_audio(image_paths, num_images, duration, output_path):
    # Set a fixed display duration for each image
    image_display_duration = duration / num_images
    
    # Create ImageSequenceClip
    video_clip = ImageSequenceClip(image_paths, durations=[image_display_duration] * num_images)
    
    # Write the final video to file
    video_clip.write_videofile(output_path, fps=24, codec='libx264', preset='ultrafast')

if __name__ == '__main__':
    app.run()
