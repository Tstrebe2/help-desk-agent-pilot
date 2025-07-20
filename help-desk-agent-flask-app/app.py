from flask import Flask, render_template, request, jsonify
from llm_handler import get_llm_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("message")
    response = get_llm_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)