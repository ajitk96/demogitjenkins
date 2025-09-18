# py_high_risk.py
import sqlite3
import os
import pickle

# Hardcoded credentials (secrets exposed)
DB_PASSWORD = "supersecretpassword"

def sql_injection(username, password):
    # ❌ SQL Injection via string interpolation
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    q = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    cur.execute(q)
    rows = cur.fetchall()
    conn.close()
    return rows

def command_injection(user_input):
    # ❌ Command injection by concatenating user input
    os.system("ping -c 1 " + user_input)

def insecure_deserialize(data):
    # ❌ Unsafe deserialization using pickle.loads on untrusted data
    obj = pickle.loads(data)
    return obj

if __name__ == "__main__":
    # Example unsafe calls (do not run with real malicious input)
    sql_injection("admin", "password")
    command_injection("127.0.0.1")
    insecure_deserialize(b"")  # intentionally left blank for scanner
