from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import config
from groq import Groq

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

client = Groq(api_key=os.environ.get("GROQ-API-KEY") or "your-groq-key-here")

def build_system_prompt():
    prompt = f"You are {config.BOT_NAME}, a friendly AI assistant for {config.BUSINESS_NAME}.\n\n"
    prompt += f"About the business: {config.BUSINESS_DESCRIPTION}\n\n"
    prompt += f"Key info:\n{config.BUSINESS_FAQ}"
    return prompt

@app.route("/")
def home():
    return jsonify({"status": "running", "bot": config.BOT_NAME})

@app.route("/bot")
def bot():
    return app.send_static_file("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data["messages"]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": build_system_prompt()}] + messages,
        max_tokens=500
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print(f"🤖 {config.BOT_NAME} is running!")
    print("📡 Server: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
```

Also add `groq` to `requirements.txt` on GitHub:
```
flask==3.1.3
flask-cors==6.0.2
anthropic==0.84.0
groq
