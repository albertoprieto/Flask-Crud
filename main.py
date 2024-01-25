from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __init__(self, username, email, address, phone):
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone

def initialize_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    mode = "Add"
    return jsonify({'mode': mode})

@app.route('/records')
def get_users():
    users_list = User.query.all()
    users_json = [{'id': user.id, 'username': user.username, 'email': user.email, 'address': user.address, 'phone': user.phone} for user in users_list]
    return jsonify(users_json)

@app.route('/add', methods=['POST'])
def add_user():
    new_id = request.form.get("id")
    new_name = request.form.get("username")
    new_email = request.form.get("email")
    new_address = request.form.get("address")
    new_phone = request.form.get("phone")
    print(new_id)
    if not new_id:
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            return jsonify({'error': "A user with that email already exists."}), 400

    try:
        if new_id:
            user = User.query.get(new_id)
            if not user:
                return jsonify({'error': 'User not found.'}), 404
            user.username = new_name
            user.email = new_email
            user.address = new_address
            user.phone = new_phone
        else:
            new_user = User(
                username=new_name,
                email=new_email,
                address=new_address,
                phone=new_phone,
            )
            db.session.add(new_user)

        db.session.commit()
        return jsonify({"Record added successfully!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': "A user with that email already exists."}), 400

@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('id')
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': "Record deleted successfully."}), 200

@app.route('/edit', methods=['POST'])
def edit_user():
    user_id = request.form.get('id')
    user = User.query.get_or_404(user_id)
    new_name = request.form.get("username", user.username)
    new_email = request.form.get("email", user.email)
    new_address = request.form.get("address", user.address)
    new_phone = request.form.get("phone", user.phone)

    user.username = new_name
    user.email = new_email
    user.address = new_address
    user.phone = new_phone

    try:
        db.session.commit()
        user_json = {'id': user.id, 'username': user.username, 'email': user.email, 'address': user.address, 'phone': user.phone}
        mode = "Modify"
        return jsonify({'user': user_json, 'mode': mode}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
