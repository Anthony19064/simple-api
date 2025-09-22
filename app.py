from flask import Flask, jsonify

app = Flask(__name__)

# API: /getcode
@app.route("/getcode", methods=["GET"])
def getcode():
    return jsonify({"result": "Hello World "})   

@app.route("/plus/<a>/<b>", methods=["GET"])
def plus(a, b):
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        return jsonify({"error": "Invalid numbers"}), 400
    return jsonify({"result": a + b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
