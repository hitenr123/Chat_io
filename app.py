from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username,email,password)
        )
        conn.commit()
        return jsonify({"status":"success"})
    except:
        return jsonify({"status":"user_exists"})



# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = cursor.fetchone()

    if user:
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"invalid"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)