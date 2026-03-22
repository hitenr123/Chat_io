from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector

app = Flask(__name__)
CORS(app)


# ===== DATABASE CONNECTION =====
def get_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=int(os.getenv("MYSQLPORT"))
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


# ===== TEST ROUTE =====
@app.route("/")
def home():
    return {"message": "API Running"}

@app.route("/dbtest")
def dbtest():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()

        return {"message": "Database Connected"}

    except Exception as e:
        return {"error": str(e)}

# ===== REGISTER =====
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        conn = get_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # check duplicate username
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"status": "exists"})

        # insert new user
        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (username, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        print("Register error:", e)
        return jsonify({"error": str(e)}), 500


# ===== LOGIN =====
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        conn = get_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "invalid"})

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": str(e)}), 500
    


# ===== RUN APP =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)