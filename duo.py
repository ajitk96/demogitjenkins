# flask_rce_ssrf_sql_deser.py
from flask import Flask, request, send_file
import sqlite3, subprocess, pickle, requests, os

app = Flask(__name__)

# Hardcoded secret (will be flagged)
API_TOKEN = "super-secret-token-123"

def get_db():
    conn = sqlite3.connect("app.db")
    return conn

@app.route("/login", methods=["POST"])
def login():
    # ❌ SQL Injection: building SQL with string interpolation
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    q = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
    cur = get_db().cursor()
    cur.execute(q)
    row = cur.fetchone()
    return {"user": row[0] if row else None}

@app.route("/ping")
def ping():
    # ❌ Command injection via shell=True
    host = request.args.get("host", "127.0.0.1")
    # intentionally using shell and concatenation to trigger scanners
    subprocess.run(f"ping -c 1 {host}", shell=True)
    return "pinged"

@app.route("/fetch")
def fetch():
    # ❌ SSRF: fetching a user-supplied URL directly
    url = request.args.get("url")
    r = requests.get(url, timeout=3)
    return r.text[:500]

@app.route("/upload", methods=["POST"])
def upload():
    # ❌ Path traversal / arbitrary file write if filename not sanitized
    f = request.files["file"]
    filename = request.form.get("filename", f.filename)
    path = os.path.join("/tmp/uploads", filename)
    f.save(path)
    return {"saved": path}

@app.route("/deserialize", methods=["POST"])
def deserialize():
    # ❌ Unsafe deserialization: untrusted pickle.loads
    data = request.get_data()
    obj = pickle.loads(data)
    return {"type": str(type(obj))}

if __name__ == "__main__":
    app.run(debug=True)
