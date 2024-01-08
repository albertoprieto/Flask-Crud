from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os

class AppServer(Flask):
    def __init__(self, *args, **kwargs):
        super(AppServer, self).__init__(*args, **kwargs)
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_database.db'
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        UPLOAD_FOLDER = 'static/images/'
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        self.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.db = SQLAlchemy(self)

    @staticmethod
    def initialize_db():
        with app.app_context():
            app.db.create_all()

app = AppServer(__name__)

class User(app.db.Model):
    __tablename__ = 'new'
    id = app.db.Column(app.db.Integer, primary_key=True)
    username = app.db.Column(app.db.String(80), unique=True)
    email = app.db.Column(app.db.String(80), unique=True)
    address = app.db.Column(app.db.String(150), nullable=False)
    phone = app.db.Column(app.db.String(15), nullable=False)
    foto = app.db.Column(app.db.String(255))

    def __init__(self, username, email, address, phone, foto):
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.foto = foto

@app.route('/')
def index():
    user = 'null'
    mode = "Agregar"
    return render_template('index.html', user=user, mode=mode)

@app.route('/registros')
def users():
    users_list = User.query.all()
    return render_template('table.html', users=users_list)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/agregar', methods=['POST', 'GET'])
def user_added():
    new_id = request.form.get("id")
    new_name = request.form.get("username")
    new_email = request.form.get("email")
    new_address = request.form.get("address")
    new_phone = request.form.get("phone")
    foto = request.files['foto']

    if foto.filename == '':
        foto_path = None
    elif foto and allowed_file(foto.filename):
        foto_filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
    else:
        return "Formato de archivo no válido. Permitidos: png, jpg, jpeg, gif."

    if new_id:
        user = User.query.get(new_id)
        if user:
            try:
                user.username = new_name
                user.email = new_email
                user.address = new_address
                user.phone = new_phone
                user.foto = foto_path
                app.db.session.commit()
                message = "Registro editado correctamente!"
                new_user = None
            except IntegrityError:
                app.db.session.rollback()
                message = "Ya existe un usuario con ese correo electrónico."
        else:
            message = 'Usuario no encontrado'
            new_user = None
    else:
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            message = "Ya existe un usuario con ese correo electrónico."
            new_user = None
        else:
            new_user = User(
                username=new_name,
                email=new_email,
                address=new_address,
                phone=new_phone,
                foto=foto_path
            )
            try:
                app.db.session.add(new_user)
                app.db.session.commit()
                message = "Registro agregado!"
            except IntegrityError:
                app.db.session.rollback()
                message = "Ya existe un usuario con ese correo electrónico."

    return render_template('add-edit.html', user=new_user, message=message)

@app.route('/delete', methods=['POST'])
def delete_user():
    id = request.form['id']
    user = User.query.get_or_404(id)
    app.db.session.delete(user)
    app.db.session.commit()
    message = "Registro eliminado correctamente."
    return redirect('/registros')

@app.route('/edit', methods=['POST'])
def edit_user():
    id = request.form['id']
    user = User.query.get_or_404(id)
    mode = "Modificar"
    return render_template('index.html', user=user, mode=mode)

if __name__ == '__main__':
    app.initialize_db()
    app.run(debug=True)
    