from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("auth.html", initial_state='cadastro') 

@app.route("/login")
def login():
    return render_template("auth.html", initial_state='login') 

@app.route("/analyze", methods=["POST"])
def analyze_image():
    image_url = request.form.get("image_url")

    response = requests.post("http://127.0.0.1:5001/analyze", json={"image_url": image_url})

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Falha ao analisar a imagem"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)