import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

JARVIS_SYSTEM_PROMPT = """You are JARVIS, a highly intelligent, calm, and witty AI assistant 
inspired by Tony Stark's assistant. You address the user respectfully (e.g., "Sir"), 
speak concisely, and occasionally add subtle wit. You help with any task the user asks — 
answering questions, summarizing text, giving explanations, or just chatting. 
Keep responses clear and not overly long unless detail is needed."""

# In-memory conversation store (single-user demo; resets on restart)
conversation_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    conversation_history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system=JARVIS_SYSTEM_PROMPT,
        messages=conversation_history
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})

    # Keep history from growing unbounded
    if len(conversation_history) > 20:
        del conversation_history[:2]

    return jsonify({"reply": reply})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[
            {"role": "user", "content": f"Summarize this in 3 lines:\n\n{text}"}
        ]
    )
    summary = response.content[0].text
    return jsonify({"summary": summary})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
