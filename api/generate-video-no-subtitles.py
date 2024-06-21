from flask import Flask, request, send_file, jsonify
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip, TextClip, ColorClip
import os
import tempfile

app = Flask(__name__)

@app.route('/api/generate-video-with-subtitles', methods=['POST'])
def genVideoWithSubtitles():
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

    # Load the generated video and overlay captions generated from the audio
    video_clip = VideoFileClip(temp_video_path)
    final_video_with_captions = overlay_captions_with_segments(video_clip, createTranscriptions(audio_path))

    # Save the final video with captions
    final_output_path = os.path.join(temp_dir, f'final_video_with_captions_{uid}.mov')
    final_video_with_captions.write_videofile(final_output_path, fps=24, codec='libx264', preset='ultrafast')

    return send_file(final_output_path, as_attachment=True, download_name='final_video_with_captions.mov')

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

def overlay_captions_with_segments(video_clip, segments):
    caption_clips = []
    bar_height = 160  # Adjust this value as needed for the background bar height
    background_bar = ColorClip(size=(video_clip.size[0], bar_height),
                               color=(0, 0, 0, 128),
                               duration=video_clip.duration).set_position(
                                   ("bottom"))

    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        duration = end_time - start_time

        # Wrap text to fit a certain width
        wrapped_text = wrap_text(text, max_width=60)  # Adjust max_width as needed

        # Create a text clip for the wrapped text
        text_clip = TextClip(wrapped_text,
                             fontsize=36,
                             color='white',
                             font='Arial-Bold',
                             stroke_color='black',
                             stroke_width=1,
                             align="South",
                             method='caption',
                             size=(video_clip.w,
                                   bar_height)).set_start(start_time).set_duration(
                                       duration).set_position('bottom')

        caption_clips.append(text_clip)

    final_video = CompositeVideoClip([video_clip, background_bar] +
                                     caption_clips,
                                     size=video_clip.size)
    return final_video

def createTranscriptions(audio_path):
    # Function to create transcriptions from audio file
    pass

def wrap_text(text, max_width):
    """Wrap text to ensure each line is no longer than max_width."""
    # Use textwrap to wrap text. This returns a list of wrapped lines.
    wrapped_lines = textwrap.wrap(text, width=max_width)

    # Join the list of lines into a single string with line breaks.
    wrapped_text = '\n'.join(wrapped_lines)
    return wrapped_text

if __name__ == '__main__':
    app.run()


