import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize the Gemini client 
client = genai.Client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"reply": "Please enter a valid message."}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message,
        )
        bot_reply = response.text
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error communicating with AI: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)