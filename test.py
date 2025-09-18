import sqlite3
import os

def vulnerable_login(username, password):
    # ❌ SQL Injection vulnerability
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)  # CodeQL will flag this
    result = cursor.fetchall()
    conn.close()
    return result

def run_system_command(user_input):
    # ❌ Command Injection vulnerability
    os.system("echo " + user_input)  # CodeQL will flag this

if __name__ == "__main__":
    # Sample test calls
    vulnerable_login("admin", "password123")
    run_system_command("hello; rm -rf /")
