from flask import Flask, send_file
from moviepy.editor import TextClip, CompositeVideoClip
import tempfile
import os

app = Flask(__name__)

@app.route('/api/hello-world-test ')
def hello_world_video():
    # Create a text clip
    text_clip = TextClip("Hello World", fontsize=70, color='white', bg_color='black', size=(640, 480))

    # Set the duration to 1 second
    text_clip = text_clip.set_duration(1)

    # Create a CompositeVideoClip if you want to add more clips or effects
    video_clip = CompositeVideoClip([text_clip])

    # Output file path
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f'final_video.mov')

    # Write the video file
    video_clip.write_videofile(output_path, fps=24)

    # Send the video file as a response
    return send_file(output_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
