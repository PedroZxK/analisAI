# app.py

# 1. Importa a classe Flask e a função render_template
from flask import Flask, render_template

# 2. Cria a instância do aplicativo Flask e a atribui à variável 'app'
app = Flask(__name__)

# 3. Define a rota principal (a URL /)
@app.route("/")
def home():
    # 4. Retorna a renderização do arquivo 'index.html'
    return render_template("index.html")

# 5. Inicia o servidor, garantindo que 'app' esteja definida
if __name__ == "__main__":
    app.run(debug=True)