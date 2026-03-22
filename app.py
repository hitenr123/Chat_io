from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
import urllib.parse
import mysql.connector

app = Flask(__name__)
CORS(app)   # enable CORS


# ===== DATABASE CONNECTION =====
def get_db():
    try:
        url = os.getenv("DATABASE_URL")
        parsed = urllib.parse.urlparse(url)

        print("Connecting to DB...")
        print("HOST:", parsed.hostname)
        print("USER:", parsed.username)
        print("DB:", parsed.path[1:])
        print("PORT:", parsed.port)

        conn = mysql.connector.connect(
            host=parsed.hostname,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],
            port=parsed.port
        )

        print("DATABASE CONNECTED ✅")
        return conn

    except Exception as e:
        print("Database connection error:", e)
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
    
@app.route("/dbtest")
def dbtest():
    conn = get_db()
    if conn:
        return "Database Connected"
    else:
        return "Database Failed"

@app.route("/env")
def env():
    return {
        "DATABASE_URL": str(os.getenv("DATABASE_URL"))
    }
    
@app.route("/parsetest")
def parsetest():
    url = os.getenv("DATABASE_URL")

    if not url:
        return {"error": "DATABASE_URL not found"}

    parsed = urllib.parse.urlparse(url)

    return {
        "host": parsed.hostname,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path[1:],   # removes /
        "port": parsed.port
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)