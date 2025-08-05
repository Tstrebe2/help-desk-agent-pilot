# app.py
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from llm_handler import get_agent_response
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("message")
    response = get_agent_response(user_input)
    return jsonify({"response": response})


@app.route("/ticket/<ticket_id>")
def ticket_detail(ticket_id: str):
    """Display an individual help desk ticket."""
    db_path = "../../datasets/help-desk-tickets/sqlite_db/help_desk_agent.sqlite3"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM va_helpdesk_tickets_sample_realistic WHERE TicketID = ?",
        (ticket_id,),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return "Ticket not found", 404
    return render_template("ticket.html", ticket=dict(row))


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
