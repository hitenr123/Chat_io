from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
import urllib.parse

app = Flask(__name__)
CORS(app)


# ===== DATABASE CONNECTION =====
def get_db():
    try:
        url = os.getenv("DATABASE_URL")
        parsed = urllib.parse.urlparse(url)

        conn = mysql.connector.connect(
            host=parsed.hostname,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],   # remove '/'
            port=parsed.port
        )

        return conn

    except Exception as e:
        print("DB ERROR:", e)
        return None


# ===== TEST ROUTE =====
@app.route("/dbtest")
def dbtest():
    conn = get_db()
    if conn:
        return "Database Connected ✅"
    else:
        return "Database Failed ❌"


# ===== REGISTER =====
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        username = data["username"]
        email = data["email"]
        password = data["password"]

        conn = get_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

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


# ===== LOGIN =====
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        conn = get_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

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


# ===== RUN APP =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)