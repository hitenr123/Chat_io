from flask import Flask, render_template, request, jsonify
import os
import mysql.connector

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (data["username"], data["email"], data["password"])
        )

        conn.commit()
        conn.close()

        return {"status":"success"}

    except Exception as e:
        return {"error": str(e)}


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (data["username"], data["password"])
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return {"status":"success"}
        else:
            return {"status":"invalid"}
    
    except Exception as e:
        return {"error": str(e)}
    
@app.route("/testdb")
def testdb():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    return "Database connected!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)