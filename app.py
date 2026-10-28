import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize the Gemini client using the environment variable on Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
  user_message = request.json.get("message")
  if not user_message:
    return jsonify({"error": "No message provided"}), 400

  try:
    # Generate response using the recommended gemini-2.5-flash model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
    )
    return jsonify({"response": response.text})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
