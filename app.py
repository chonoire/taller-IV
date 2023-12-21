# En app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from modelos import db, User, Estudiante
from reportlab.pdfgen import canvas
import io

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
        page = request.args.get('page', 1, type=int)

        # Obtener los criterios de filtrado desde los parámetros de la solicitud
        filtro_nombre = request.args.get('filtro_nombre', '', type=str)
        filtro_apellido = request.args.get('filtro_apellido', '', type=str)
        filtro_curso = request.args.get('filtro_curso', '', type=str)
        filtro_cedula = request.args.get('filtro_cedula', '', type=str)

        # Filtrar estudiantes según los criterios
        estudiantes_query = Estudiante.query.filter(Estudiante.nombre.ilike(f'%{filtro_nombre}%'))
        estudiantes_query = estudiantes_query.filter(Estudiante.apellido.ilike(f'%{filtro_apellido}%'))
        estudiantes_query = estudiantes_query.filter(Estudiante.curso.ilike(f'%{filtro_curso}%'))
        estudiantes_query = estudiantes_query.filter(Estudiante.cedula.ilike(f'%{filtro_cedula}%'))

        # Paginar los resultados
        estudiantes_paginados = estudiantes_query.paginate(page=page, per_page=10)

        return render_template('inicio.html', usuario=usuario, estudiantes=estudiantes_paginados,
                               filtro_nombre=filtro_nombre, filtro_curso=filtro_curso,
                               filtro_cedula=filtro_cedula, filtro_apellido=filtro_apellido)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "info")
    return redirect(url_for("login"))

@app.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre= request.form.get("nombre")
        apellido=request.form.get("apellido")
        cedula=request.form.get("cedula")
        curso=request.form.get("curso")
        nota=request.form.get("nota")

        # Crear una nueva instancia de Estudiante
        nuevo_estudiante = Estudiante(nombre = nombre, apellido = apellido, cedula = cedula, curso = curso, nota=nota)

        # Agregar el estudiante a la base de datos
        db.session.add(nuevo_estudiante)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route("/eliminar/<id>")
def eliminar(id):
    #eliminar por id
    estudiante = Estudiante.query.get(id)
    #eliminar
    db.session.delete(estudiante)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/editar/<id>", methods=["GET","POST"])
def editar(id):
    estudiante = Estudiante.query.get(id)
    if request.method == "POST":
        nombre= request.form.get("nombre")
        apellido=request.form.get("apellido")
        cedula=request.form.get("cedula")
        curso=request.form.get("curso")
        nota=request.form.get("nota")
        #cargar la info
        estudiante.nombre= nombre
        estudiante.apellido = apellido
        estudiante.cedula = cedula
        estudiante.curso = curso
        estudiante.nota = nota
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("editar.html", estudiante = estudiante)

def generar_pdf():
    # Crear un buffer en memoria para almacenar el PDF
    buffer = io.BytesIO()

    # Crear un documento PDF con reportlab
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Informe de Notas Bajas")

    # Obtener estudiantes con notas bajas (menores a 3)
    estudiantes_notas_bajas = Estudiante.query.filter(Estudiante.nota < 3).all()

    # Agregar información de estudiantes con notas bajas al PDF
    y_position = 730
    for estudiante in estudiantes_notas_bajas:
        y_position -= 15
        pdf.drawString(100, y_position, f"{estudiante.nombre} {estudiante.apellido}: {estudiante.nota}")

    # Guardar el documento PDF
    pdf.showPage()
    pdf.save()

    # Reiniciar el buffer y devolver los datos binarios del PDF
    buffer.seek(0)
    return buffer.read()

# Ruta para el informe de notas bajas
@app.route("/reporte_notas_bajas")
def reporte_notas_bajas():
    # Generar el PDF y devolverlo como respuesta
    pdf_filename = 'informe_notas_bajas.pdf'
    response = make_response(generar_pdf())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={pdf_filename}'
    return response

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
