from flask import Flask, render_template, request, jsonify, session
from chatbot import load_intents, get_response, validate_message

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # needed for session (conversation memory)

data = load_intents()


@app.route("/")
def home():
    session["history"] = []        # start a fresh conversation
    session["fallback_count"] = 0
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message", "")

    # 1. Validate the user's input
    ok, error = validate_message(message)
    if not ok:
        return jsonify({"reply": error})

    # 2. Get the bot's reply
    reply, tag = get_response(message, data)

    # 3. Conversation handling: if bot fails 2 times in a row, suggest human support
    if tag == "fallback":
        session["fallback_count"] = session.get("fallback_count", 0) + 1
        if session["fallback_count"] >= 2:
            reply = "I am still unable to help. Please email support@StyleHub.com to talk to our team."
    else:
        session["fallback_count"] = 0

    # 4. Save the conversation history (last 20 messages)
    history = session.get("history", [])
    history.append({"user": message, "bot": reply})
    session["history"] = history[-20:]

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
