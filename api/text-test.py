from flask import Flask, request, send_file, jsonify
import os
import tempfile

app = Flask(__name__)

@app.route('/api/text-test', methods=['GET'])
def test_tmp_write():
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, 'test_temp_file.txt')

    # Write to the temp file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("This is a test to see if the /tmp directory is writable.\n")
    
    # Read from the temp file
    with open(temp_file_path, 'r') as temp_file:
        content = temp_file.read()
    
    print(f"Contents of the temp file: {content}")

    return jsonify({"message": "Temp file write test completed", "content": content}), 200

if __name__ == '__main__':
    app.run()