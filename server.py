from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 🔑 Coloque sua chave da API aqui
genai.configure(api_key="AIzaSyBm8NlTS10UyJARnjmb3UhpMfjYdJ8rGeI")

# Função para detectar o modelo automaticamente e evitar 404
def get_model():
    try:
        models = genai.list_models()
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                # Usa exatamente o nome detectado
                if "gemini-1.5-flash" in m.name:
                    print(f"✅ Modelo detectado: {m.name}")
                    return genai.GenerativeModel(m.name)
                if "gemini-1.0-pro" in m.name:
                    print(f"✅ Modelo detectado: {m.name}")
                    return genai.GenerativeModel(m.name)
                if "gemini-pro" in m.name:
                    print(f"✅ Modelo detectado: {m.name}")
                    return genai.GenerativeModel(m.name)
        # Fallback padrão
        print("⚠️ Nenhum modelo premium encontrado. Usando gemini-1.0-pro como padrão.")
        return genai.GenerativeModel("gemini-1.0-pro")
    except Exception as e:
        print(f"❌ Erro ao detectar modelo: {e}")
        return genai.GenerativeModel("gemini-1.0-pro")

# Inicializa o modelo
model = get_model()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"response": "Mensagem vazia recebida."})

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"⚠️ Erro: {str(e)}"})

if __name__ == "__main__":
    print("🚀 Servidor Uvee.ia iniciado em http://127.0.0.1:5000")
    app.run(debug=True)
