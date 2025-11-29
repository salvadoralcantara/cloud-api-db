import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "34.170.234.238"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "apiuser"),
    "password": os.environ.get("DB_PASS", "ApiPass123!"),
    "database": os.environ.get("DB_NAME", "proyecto3"),
    "connection_timeout": 10
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (name, email))
        db.commit()
        cur.close()
        db.close()
        return jsonify({"status":"ok","data":data}), 200
    except Exception as e:
        return jsonify({"status":"error","msg":str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)