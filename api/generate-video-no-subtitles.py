from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from moviepy.editor import ImageSequenceClip
import os
import io
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-video-no-subtitles', methods=['POST'])
def genVideoNoSubtitles():
    uid = request.form['uid']
    strNumImages = request.form['imageCount']
    numImages = int(strNumImages)

    # Paths for temporary storage
    temp_dir = tempfile.gettempdir()
    image_paths = [os.path.join(temp_dir, f'image_{index}_{uid}.png') for index in range(numImages)]
    print(image_paths)

    # Save the uploaded image files
    for index in range(numImages):
        if f'image_{index}' not in request.files:
            return jsonify({"error": f"Image file image_{index} is required"}), 400
        image_file = request.files[f'image_{index}']
        image_file.save(image_paths[index])
        print(f'image{index} saved!')

    # Create video without audio
    temp_video_path = os.path.join(temp_dir, f'final_video_{uid}.mov')
    print(temp_video_path)
    create_video_without_audio(image_paths, numImages, temp_video_path)

    return send_file(temp_video_path, as_attachment=True, download_name='final_video.mov')

def create_video_without_audio(image_paths, num_images, output_path):
    # Set a fixed display duration for each image
    image_display_duration = 1  # Display each image for 1 second

    # Create ImageSequenceClip
    video_clip = ImageSequenceClip(image_paths, durations=[image_display_duration] * num_images)

    # Write the final video to file
    video_clip.write_videofile(output_path, fps=24, codec='libx264', preset='ultrafast')

if __name__ == '__main__':
    app.run()
