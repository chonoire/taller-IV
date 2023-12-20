# En app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from modelos import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "tu_clave_secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["username"] = username
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

@app.route("/inicio")
def dashboard():
    if "username" in session:
        # Recuperar detalles del usuario actualmente autenticado
        username = session["username"]
        usuario = User.query.filter_by(username=username).first()

        return render_template("inicio.html", usuario=usuario)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
