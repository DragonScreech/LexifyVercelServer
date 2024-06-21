from flask import Flask, request, send_file, jsonify
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile

app = Flask(__name__)

@app.route('/api/generate-video-no-subtitles', methods=['POST'])
def genVideoNoSubtitles():
    uid = request.form['uid']
    strNumImages = request.form['imageCount']
    numImages = int(strNumImages)

    # Paths for temporary storage
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, f'speech_{uid}.mp3')
    image_paths = [os.path.join(temp_dir, f'image_{index}_{uid}.png') for index in range(numImages)]

    # Save the uploaded audio file
    if 'audio' not in request.files:
        return jsonify({"error": "Audio file is required"}), 400
    audio_file = request.files['audio']
    audio_file.save(audio_path)

    # Save the uploaded image files
    for index in range(numImages):
        if f'image_{index}' not in request.files:
            return jsonify({"error": f"Image file image_{index} is required"}), 400
        image_file = request.files[f'image_{index}']
        image_file.save(image_paths[index])

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



