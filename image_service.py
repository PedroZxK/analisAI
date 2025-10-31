from flask import Flask, request, jsonify
import requests
import io
import os
from google.cloud import vision
from google.cloud import translate_v2 as translate

app = Flask(__name__)

HOST = "0.0.0.0"
PORT = 5001

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coral-arbor-476800-b0-e59e1d4cd0e2.json"

try:
    vision_client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
except Exception as e:
    print(f"ERRO CRÍTICO: Não foi possível inicializar os clientes Google. Verifique a chave JSON. {e}")

def analyze_image_from_bytes(image_bytes):
    
    print(f"Serviço (porta {PORT}): Iniciando análise (VISÃO)...")

    image = vision.Image(content=image_bytes)
    features = [
        {"type_": vision.Feature.Type.LABEL_DETECTION, "max_results": 10},
        {"type_": vision.Feature.Type.WEB_DETECTION, "max_results": 5}
    ]
    
    request_data = {
        "image": image,
        "features": features,
    }
    
    try:
        response = vision_client.annotate_image(request=request_data)
    except Exception as e:
        print(f"Erro na API Vision: {e}")
        return None, "Falha ao analisar a imagem."

    
    tags_en = [
        label.description for label in response.label_annotations 
        if label.score > 0.80
    ]
    if not tags_en and response.label_annotations:
        tags_en = [label.description for label in response.label_annotations[:3]]

    description_en = "Não foi possível gerar uma descrição."
    if response.web_detection.best_guess_labels:
        description_en = response.web_detection.best_guess_labels[0].label
    
    print(f"Serviço (porta {PORT}): Traduzindo {len(tags_en) + 1} termos para PT...")

    if not tags_en and description_en == "Não foi possível gerar uma descrição.":
        return [], description_en

    
    strings_to_translate = [description_en] + tags_en
    
    try:
        translation_results = translate_client.translate(
            strings_to_translate, 
            target_language="pt"
        )
        
        
        description_pt = translation_results[0]['translatedText'].capitalize()
        tags_pt = [result['translatedText'] for result in translation_results[1:]]

    except Exception as e:
        print(f"Erro na API Translate: {e}")
        
        description_pt = description_en.capitalize()
        tags_pt = tags_en

    print(f"Serviço (porta {PORT}): Análise concluída. Tags: {tags_pt}")
    
    return tags_pt, description_pt

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
    print(f"--- Iniciando Microsserviço de Análise (VISÃO + TRADUÇÃO) ---")
    print(f"Carregando credenciais...")
    app.run(host=HOST, port=PORT, debug=True)