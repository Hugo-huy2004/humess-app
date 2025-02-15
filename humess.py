from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Dùng để bảo mật session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Bảng User để lưu thông tin tài khoản
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(6), nullable=False)  # Mật khẩu đúng 6 số

# Bảng Message để lưu tin nhắn
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(500), nullable=False)

# Tạo database nếu chưa có
with app.app_context():
    db.create_all()

# Trang chủ
@app.route("/")
def home():
    return render_template("home.html")

# Trang đăng ký
@app.route("/signup")
def register_page():
    return render_template("signup.html")

# Trang đăng nhập
@app.route("/login")
def login_page():
    return render_template("login.html")

# Trang tra cứu thông tin
@app.route("/investigation")
def investigation_page():
    return render_template("investigation.html")

# Xử lý đăng ký tài khoản
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    email = request.form["email"]
    gender = request.form["gender"]
    address = request.form["address"]
    password = request.form["password"]

    if len(password) != 6 or not password.isdigit():
        return "Mật khẩu phải có đúng 6 số!", 400

    new_user = User(name=name, dob=dob, phone=phone, email=email, gender=gender, address=address, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("home"))

# Xử lý đăng nhập
@app.route("/login", methods=["POST"])
def login():
    phone = request.form["phone"]
    password = request.form["password"]
    user = User.query.filter_by(phone=phone, password=password).first()
    if user:
        session["phone"] = user.phone
        return redirect(url_for("mess"))
    else:
        return "Sai số điện thoại hoặc mật khẩu!", 400

# Trang tin nhắn
@app.route("/mess")
def mess():
    if "phone" not in session:
        return redirect(url_for("home"))
    
    messages = Message.query.filter_by(receiver=session["phone"]).all()
    return render_template("mess.html", messages=messages)

# Gửi tin nhắn
@app.route("/send_message", methods=["POST"])
def send_message():
    if "phone" not in session:
        return redirect(url_for("home"))

    receiver = request.form["receiver"]
    content = request.form["content"]
    new_message = Message(sender=session["phone"], receiver=receiver, content=content)
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for("mess"))

# Tìm kiếm thông tin người dùng
@app.route("/investigation", methods=["POST"])
def investigation():
    user = None
    phone = request.form["phone"]
    user = User.query.filter_by(phone=phone).first()
    return render_template("investigation.html", user=user)

# Đăng xuất
@app.route("/logout")
def logout():
    session.pop("phone", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
