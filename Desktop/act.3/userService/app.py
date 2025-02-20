from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User  # Import db and User model

# Initialize Flask app
app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_service.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Create all tables if they do not exist
with app.app_context():
    db.create_all()  # This ensures the tables are created in the database.

# Route for user registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.as_dict()), 201

# Route to get user details
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.as_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
