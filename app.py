from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
import urllib.parse

app = Flask(__name__)
CORS(app)   # enable CORS


def get_db():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise ValueError("DATABASE_URL not found")

    parsed = urllib.parse.urlparse(url)

    return mysql.connector.connect(
        host=parsed.hostname,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:],
        port=parsed.port
    )
    
print(os.getenv("DATABASE_URL"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        username = data.get("username")
        password = data.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "invalid"})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)