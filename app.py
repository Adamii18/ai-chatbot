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
    return app.send_static_file("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data["messages"]
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": """You are Jaidasco, the AI assistant for Jaidatech Cafe Business Centre located in Barnawa, Dan Alhaji Street, Kaduna South, Kaduna State, Nigeria.

We offer the following services:
- Printing, Scanning, Photocopy, Laminating
- Online Registration (JAMB, WAEC, NECO, NIN, etc)
- Passport and ID Card processing
- Students Accessories: Books, Pens, Rulers, Math sets, Erasers, Envelopes and more

Business Hours: Monday to Saturday, 8:00am to 9:00pm

Contact us:
- Phone: +234-8064458456 or +234-7018971514
- Email: jaidatechventures@gmail.com

For pricing, kindly contact us directly via phone or email and we will give you the best rates. You can also visit us in person at our shop.

Always be friendly, helpful and professional. Answer questions about our services, direct customers to contact us for pricing, and encourage them to visit our shop."""}] + messages,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    print("Aria is running!")
    app.run(debug=True, host="0.0.0.0", port=5000)


