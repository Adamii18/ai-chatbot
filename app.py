from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import config

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

def build_system_prompt():
    prompt = f"You are {config.BOT_NAME}, a friendly AI assistant for {config.BUSINESS_NAME}.\n\n"
    prompt += f"About the business: {config.BUSINESS_DESCRIPTION}\n\n"
    prompt += f"Key info:\n{config.BUSINESS_FAQ}"
    return prompt

@app.route("/")
def home():
    return jsonify({"status": "running", "bot": config.BOT_NAME})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data["messages"]
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=build_system_prompt(),
        messages=messages
    )
    
    reply = response.content[0].text
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print(f"🤖 {config.BOT_NAME} is running!")
    print("📡 Server: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)