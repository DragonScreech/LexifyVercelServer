from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello():
    some_param = request.form.get('param')
    return jsonify(param="here is the param" + some_param)

if __name__ == "__main__":
    app.run()

