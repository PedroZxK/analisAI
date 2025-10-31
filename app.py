from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Rota principal - página inicial
@app.route("/")
def home():
    return render_template("index.html")

# Rota de Cadastro (que configuramos no index.html)
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html") 

# Rota de Login (que configuramos no index.html e cadastro.html)
@app.route("/login")
def login():
    # Você precisará criar este arquivo login.html
    return render_template("login.html") 

# Rota para enviar imagem ao microsserviço de análise
@app.route("/analyze", methods=["POST"])
def analyze_image():
    image_url = request.form.get("image_url")

    # Envia requisição para o microsserviço de análise
    # Lembre-se que este outro serviço (na porta 5001) precisa estar rodando
    response = requests.post("http://127.0.0.1:5001/analyze", json={"image_url": image_url})

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Falha ao analisar a imagem"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)