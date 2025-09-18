import os, pickle, subprocess, sqlite3

# Hardcoded secret (always triggers)
API_KEY = "ghp_1234567890abcdefghijklmnop"

# SQL injection
def login(user, pwd):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    # Unsafe query: untrusted input directly in SQL
    cur.execute("SELECT * FROM users WHERE name = '" + user + "' AND pass = '" + pwd + "';")
    return cur.fetchall()

# Command injection
def run_command(cmd):
    os.system(cmd)   # dangerous

# Subprocess shell injection
def run_subprocess(cmd):
    subprocess.Popen(cmd, shell=True)   # dangerous

# Insecure deserialization
def deserialize(data):
    return pickle.loads(data)   # dangerous
