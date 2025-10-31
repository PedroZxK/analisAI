from flask import Flask, request, jsonify
import requests
import io
import os

from google.cloud import vision

app = Flask(__name__)

HOST = "0.0.0.0"
PORT = 5001

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coral-arbor-476800-b0-e59e1d4cd0e2.json"

def analyze_image_from_bytes(image_bytes):
    """
    Esta função agora chama a API Google Cloud Vision para obter
    tags e descrições reais da imagem.
    """
    
    print(f"Serviço (porta {PORT}): Iniciando análise REAL com Google Vision...")

    try:
        client = vision.ImageAnnotatorClient()
    except Exception as e:
        print(f"Erro ao inicializar o cliente Vision (verifique a chave JSON): {e}")
        return None, "Falha ao autenticar com a API de Visão."

    image = vision.Image(content=image_bytes)

    features = [
        {"type_": vision.Feature.Type.LABEL_DETECTION, "max_results": 10},
        {"type_": vision.Feature.Type.WEB_DETECTION, "max_results": 5}
    ]

    request_data = {"image": image, "features": features}
    response = client.annotate_image(request=request_data)

    tags = [
        label.description for label in response.label_annotations 
        if label.score > 0.80
    ]
    if not tags and response.label_annotations:
        tags = [label.description for label in response.label_annotations[:3]]

    description = "Não foi possível gerar uma descrição."
    if response.web_detection.best_guess_labels:
        description = response.web_detection.best_guess_labels[0].label
        description = description.capitalize()

    print(f"Serviço (porta {PORT}): Análise concluída. Tags: {tags}")
    
    return tags, description

@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    print(f"\nServiço (porta {PORT}): Requisição /analyze recebida.")
    
    data = request.get_json()
    if not data or 'image_url' not in data:
        print("Erro: Nenhuma URL de imagem fornecida.")
        return jsonify({"error": "Nenhuma URL de imagem fornecida"}), 400
    
    image_url = data['image_url']
    print(f"Serviço (porta {PORT}): Baixando imagem de: {image_url}")

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        image_bytes = response.content

        tags, description = analyze_image_from_bytes(image_bytes)
        
        if tags is None:
             return jsonify({"error": description}), 400

        return jsonify({
            "tags": tags,
            "description": description
        })

    except requests.exceptions.RequestException as e:
        print(f"Erro: Falha ao baixar a imagem. {e}")
        return jsonify({"error": f"Falha ao baixar a imagem da URL: {e}"}), 500
    except Exception as e:
        print(f"Erro: Erro interno. {e}")
        return jsonify({"error": f"Erro interno no servidor: {e}"}), 500

if __name__ == "__main__":
    print(f"--- Iniciando Microsserviço de Análise de Imagem (MODO REAL) ---")
    print(f"Carregando credenciais da API Vision...")
    app.run(host=HOST, port=PORT, debug=True)