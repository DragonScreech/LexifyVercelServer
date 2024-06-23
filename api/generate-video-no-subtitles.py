from flask import Flask, request, send_file, jsonify
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import io
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
    print(audio_path)
    image_paths = [os.path.join(temp_dir, f'image_{index}_{uid}.png') for index in range(numImages)]
    print(image_paths)

    # Save the uploaded audio file
    if 'audio' not in request.files:
        return jsonify({"error": "Audio file is required"}), 400
    audio_file = request.files['audio']
    audio_file.save(audio_path)
    print('Audio saved!')

    # Save the uploaded image files
    for index in range(numImages):
        if f'image_{index}' not in request.files:
            return jsonify({"error": f"Image file image_{index} is required"}), 400
        image_file = request.files[f'image_{index}']
        image_file.save(image_paths[index])
        print(f'image{index} saved!')

    # Create video with audio
    temp_video_path = os.path.join(temp_dir, f'final_video_{uid}.mov')
    print(temp_video_path)
    video_stream = io.BytesIO()
    create_video_with_audio(audio_path, image_paths, numImages, video_stream)
    video_stream.seek(0)

    return send_file(video_stream, as_attachment=True, download_name='final_video.mov')

def create_video_with_audio(audio_path, image_paths, num_images, output_path):
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration  # Get audio duration in seconds

    # Calculate display duration for each image
    image_display_duration = audio_duration / num_images

    # Create ImageSequenceClip
    video_clip = ImageSequenceClip(image_paths, durations=[image_display_duration] * num_images)
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video to file
    print('Output before: ' + output_path)
    video_clip.write_videofile(output_path, fps=24, codec='libx264', preset='ultrafast')
    print("Output After: " + output_path)

if __name__ == '__main__':
    app.run()



