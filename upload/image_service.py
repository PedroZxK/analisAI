from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    data = request.get_json()
    image_path = data.get("image_path")

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Imagem não encontrada"}), 400

    # Simulação de análise (poderia usar IA real)
    result = {
        "mensagem": "Análise concluída com sucesso!",
        "imagem": image_path,
        "detalhes": "A imagem parece conter uma figura ou cenário detectável."
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
