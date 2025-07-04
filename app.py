from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from chatbot_logic import get_chatbot_response

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load environment variables
load_dotenv()

@app.route("/", methods=["GET"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/send_message", methods=["POST"])
def send_message():
    # Get user input from the request
    user_input = request.json.get("user_input")

    # Get chatbot response
    system_message = "Always answer in the context of Superior University in Pakistan. When discussing fees or scholarships, always use Pakistani Rupees (PKR) — not US Dollars."
    bot_response = get_chatbot_response(system_message + user_input)

    # Update the session with user input and bot response
    if "chat_history" not in session:
        session["chat_history"] = []
    session["chat_history"].append(("user", user_input))
    session["chat_history"].append(("bot", bot_response))

    # Return the bot response as JSON
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
