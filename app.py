from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Kết nối database
def get_db_connection():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Trang chính
@app.route("/")
def home():
    return render_template("home.html")

# Trang đăng ký tài khoản
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        birthdate = request.form["birthdate"]
        phone = request.form["phone"]
        email = request.form["email"]
        gender = request.form["gender"]
        address = request.form["address"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, birthdate, phone, email, gender, address, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, birthdate, phone, email, gender, address, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))
    
    return render_template("signup.html")

# Trang đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = ? AND password = ?", (phone, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("mess"))
        else:
            return "Login failed. Invalid phone or password."

    return render_template("login.html")

# Trang hiển thị tin nhắn
@app.route("/mess")
def mess():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    conn.close()
    
    return render_template("mess.html", messages=messages)

# Tra cứu thông tin người dùng
@app.route("/investigation", methods=["GET", "POST"])
def investigation():
    user_info = None
    if request.method == "POST":
        phone = request.form["phone"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, address, gender FROM users WHERE phone = ?", (phone,))
        user_info = cursor.fetchone()
        conn.close()

    return render_template("investigation.html", user=user_info)

if __name__ == "__main__":
    app.run(debug=True)
