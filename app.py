from flask import Flask, render_template, jsonify, request, url_for
import requests
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.static_folder, 'user_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("auth.html", initial_state='cadastro') 

@app.route("/login")
def login():
    return render_template("auth.html", initial_state='login') 

@app.route("/upload")
def upload():
    return render_template("upload.html") 


@app.route("/process-image-upload", methods=["POST"])
def process_image_upload():
    """
    Orquestrador: Recebe o arquivo do cliente, salva,
    chama o microsserviço, deleta o arquivo e retorna a análise.
    """
    if 'image_file' not in request.files:
        return jsonify({"error": "Nenhum arquivo de imagem enviado"}), 400
    
    file = request.files['image_file']
    
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        try:
            file.save(filepath)
            
            file_url = url_for('static', filename=f'user_uploads/{unique_filename}', _external=True)

            microservice_url = "http://127.0.0.1:5001/analyze"
            response = requests.post(microservice_url, json={"image_url": file_url})
            
            if response.status_code == 200:
                analysis_results = response.json()
                return jsonify(analysis_results)
            else:
                return jsonify({"error": "Falha no microsserviço de análise"}), 500

        except requests.ConnectionError:
            return jsonify({"error": "Não foi possível conectar ao microsserviço de análise"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    image_url = request.json.get("image_url")
    response = requests.post("http://127.0.0.1:5001/analyze", json={"image_url": image_url})

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Falha ao analisar a imagem"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)