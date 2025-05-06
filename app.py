from flask import Flask, render_template, request, jsonify
import time
from agente import AgenteIA  # Importando a classe AgenteIA

app = Flask(__name__)

# Cria uma instância do AgenteIA
agente = AgenteIA()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")  # Mensagem do usuário enviada pelo frontend
    
    # Chama o agente para gerar a resposta
    ia_response = agente.ouvir_comando(user_message)
    
    # Simula um pequeno atraso (ajuste conforme a necessidade)
    time.sleep(1)
    
    return jsonify({"response": ia_response})

if __name__ == "__main__":
    app.run(debug=True)
