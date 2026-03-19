from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import groq

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

groq_key = os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key") or ""
client = groq.Groq(api_key=groq_key)

@app.route("/")
def home():
    return jsonify({"status": "running", "bot": "Aria", "key_set": bool(groq_key)})

@app.route("/bot")
def bot():
    return app.send_static_file("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data["messages"]
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are Jaidasco, a friendly AI assistant built by Adam Ishaq Isah. Be helpful and concise."}] + messages,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    print("Aria is running!")
    app.run(debug=True, host="0.0.0.0", port=5000)


