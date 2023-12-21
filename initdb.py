from flask import Flask
from modelos import db, User, Estudiante

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
        
        estudiante1 = Estudiante(cedula= 6270242, nombre='sofia', apellido='caceres', curso=2, nota=5)
        db.session.add(estudiante1)
        estudiante2 = Estudiante(cedula= 5544554, nombre='pedro', apellido='picapiedra', curso=1, nota=5)
        db.session.add(estudiante2)
        estudiante3 = Estudiante(cedula= 111111, nombre='sole', apellido='lopez', curso=2, nota=3)
        db.session.add(estudiante3)
        estudiante4 = Estudiante(cedula= 548765, nombre='pedro', apellido='alcaraz', curso=1, nota=4)
        db.session.add(estudiante4)
        estudiante5 = Estudiante(cedula= 548798, nombre='juan', apellido='vera', curso=2, nota=1)
        db.session.add(estudiante5)
        estudiante6 = Estudiante(cedula= 548721, nombre='sandra', apellido='lugo', curso=1, nota=4)
        db.session.add(estudiante6)
        estudiante7 = Estudiante(cedula= 653298, nombre='mira', apellido='evra', curso=3, nota=2)
        db.session.add(estudiante7)
        estudiante8 = Estudiante(cedula= 875432, nombre='lara', apellido='alcaraz', curso=3, nota=2)
        db.session.add(estudiante8)

        db.session.commit()
