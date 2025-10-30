from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Pasta onde as imagens serão salvas temporariamente
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(image_path)

    # Envia a imagem para o microsserviço de análise
    response = requests.post(
        "http://127.0.0.1:5001/analyze",
        json={"image_path": image_path}
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Erro ao analisar a imagem"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
