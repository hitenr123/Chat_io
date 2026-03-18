from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

# MySQL connection
def get_db():
    return mysql.connector.connect(
        host="hopper.proxy.rlwy.net",
        user="root",
        password="FBsCNqtdfPWnZrwbKuLsWlOlGtxABJlW",
        database="railway",
        port=40764
    )

# Home page (login)
@app.route("/login", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/chat")

    return render_template("index.html")


# Register
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Chat page
@app.route("/chat")
def chat():

    if "username" in session:
        return render_template("chat.html", username=session["username"])

    return redirect("/")


# Socket chat
@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)