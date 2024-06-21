from flask import Flask, request, send_file, jsonify
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile
import time
from firebase_admin import credentials, initialize_app, storage

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
})
initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_PROJECT_ID') + '.appspot.com'
})

bucket = storage.bucket()

def download_file_from_storage(blob_name, destination_path):
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_path)

@app.route('/api/generate-video-no-subtitles', methods=['POST'])
def genVideoNoSubtitles():
    uid = request.form['uid']
    strNumImages = request.form['imageCount']
    numImages = int(strNumImages)

    # Paths for temporary storage
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, f'speech_{uid}.mp3')
    image_paths = [os.path.join(temp_dir, f'image_{index}_{uid}.png') for index in range(numImages)]

    # Download audio and images from Firebase Storage
    download_file_from_storage(f'temp/speech_{uid}.mp3', audio_path)
    for index in range(numImages):
        download_file_from_storage(f'temp/image_{index}_{uid}.png', image_paths[index])

    # Create video with audio
    temp_video_path = os.path.join(temp_dir, f'final_video_{uid}.mov')
    create_video_with_audio(audio_path, image_paths, numImages, temp_video_path)

    return send_file(temp_video_path, as_attachment=True, download_name='final_video.mov')

def create_video_with_audio(audio_path, image_paths, num_images, output_path="final_video.mov"):
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration  # Get audio duration in seconds

    # Calculate display duration for each image
    image_display_duration = audio_duration / num_images

    # Create ImageSequenceClip
    video_clip = ImageSequenceClip(image_paths, durations=[image_display_duration] * num_images)
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video to file
    video_clip.write_videofile(output_path, fps=24, codec='libx264', preset='ultrafast')

if __name__ == '__main__':
    app.run()


