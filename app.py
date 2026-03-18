from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "running", "bot": "Aria"})

@app.route("/bot")
def bot():
    return app.send_static_file("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data["messages"]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are Aria, a friendly AI assistant. Be helpful and concise."}] + messages,
        max_tokens=500
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("Aria is running!")
    app.run(debug=True, host="0.0.0.0", port=5000)
