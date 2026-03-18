from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/chat")

    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/chat")
def chat():
    if "username" in session:
        return render_template("chat.html", username=session["username"])
    return redirect("/")

# Socket
@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)