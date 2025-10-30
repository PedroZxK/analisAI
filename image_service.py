from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    image_url = data.get("image_url")

    # Aqui é onde a API externa seria integrada
    # Exemplo com imagem de teste fornecida
    if not image_url:
        image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample16.png"

    # Simulação de análise (poderia usar uma API de IA, visão computacional etc.)
    analysis_result = {
        "image_url": image_url,
        "analysis": "A imagem contém uma pessoa sorrindo em um ambiente externo.",
        "confidence": 0.95
    }

    return jsonify(analysis_result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
