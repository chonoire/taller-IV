from flask import Flask
from modelos import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializamos la base de datos
db.init_app(app)

with app.app_context():
    # Creamos la base de datos
    db.create_all()

    # Agregamos datos de forma manual
    if not User.query.filter_by(username='admin').first():
        roles_list = ['admin', 'docente']
        usuario = User(username = 'admin', nombre = 'sofia', apellido = 'caceres')
        usuario.set_password('123')
        usuario.set_roles(['admin', 'docente'])
        db.session.add(usuario)
        db.session.commit()
