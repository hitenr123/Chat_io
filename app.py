from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
import mysql.connector
import urllib.parse

app = Flask(__name__)
CORS(app)   # enable CORS


# ===== DATABASE CONNECTION =====
def get_db():
    try:
        print("HOST:", os.getenv("MYSQLHOST"))
        print("USER:", os.getenv("MYSQLUSER"))
        print("PASS:", os.getenv("MYSQLPASSWORD"))
        print("DB:", os.getenv("MYSQLDATABASE"))
        print("PORT:", os.getenv("MYSQLPORT"))

        return mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "autorack.proxy.rlwy.net"),
            user=os.getenv("MYSQLUSER", "root"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE", "railway"),
            port=int(os.getenv("MYSQLPORT", 50880))
        )
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None

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