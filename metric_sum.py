from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/metric/<key>/", methods=["POST"])
def store_value(key):
    data = request.get_json()
    value = data.get('value', None)
    if value is not None:
        print("recieved {}".format(value))
        return {}, 200
    else:
        return {}, 500


@app.route("/metric/<key>/sum", methods=["GET"])
def read_value(key):
    return {"value": 0}, 200
