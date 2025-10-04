from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "flask-lab",
        "status": "ok",
        "message": "Hello from Dockerized Flask!"
    })

if __name__ == "__main__":
    # Dev server (only for local testing without Docker)
    app.run(host="0.0.0.0", port=5000, debug=True)
