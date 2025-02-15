import sqlite3

# Kết nối hoặc tạo mới database
conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

# Tạo bảng users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthdate TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    gender TEXT NOT NULL,
    address TEXT NOT NULL,
    password TEXT NOT NULL
);
""")

# Tạo bảng messages
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    receiver TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Database initialized successfully!")
