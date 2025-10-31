<<<<<<< HEAD
from flask import Flask, render_template

app = Flask(__name__)

=======
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Rota principal - página inicial
>>>>>>> 6ac9691b8fb199b5aba930936377d093d422a248
@app.route("/")
def home():
    return render_template("index.html")

<<<<<<< HEAD
=======
# Rota para enviar imagem ao microsserviço de análise
@app.route("/analyze", methods=["POST"])
def analyze_image():
    image_url = request.form.get("image_url")

    # Envia requisição para o microsserviço de análise
    response = requests.post("http://127.0.0.1:5001/analyze", json={"image_url": image_url})

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Falha ao analisar a imagem"}), 500


>>>>>>> 6ac9691b8fb199b5aba930936377d093d422a248
if __name__ == "__main__":
    app.run(debug=True, port=5000)
