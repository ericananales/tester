import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# URL for the user service (assuming user_service is running on port 5000)
USER_SERVICE_URL = 'http://user_service:5000/users'

# Define the Order model (Assuming it’s in the same file or import it if it's in models.py)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': self.price,
            'user_id': self.user_id
        }

# Route to create an order for a user
@app.route('/user/<int:user_id>/order', methods=['POST'])
def create_order(user_id):
    # Fetch user info from user_service
    user_response = requests.get(f'{USER_SERVICE_URL}/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    
    # The user exists, proceed with creating an order
    data = request.get_json()

    if not data.get('product_name') or not data.get('quantity') or not data.get('price'):
        return jsonify({"error": "Missing required fields"}), 400

    # Create new order
    new_order = Order(
        product_name=data['product_name'],
        quantity=data['quantity'],
        price=data['price'],
        user_id=user_id  # Use the user_id from the API response
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify(new_order.as_dict()), 201

# Route to get orders by user ID
@app.route('/user/<int:user_id>/orders', methods=['GET'])
def get_orders(user_id):
    # Fetch user info from user_service
    user_response = requests.get(f'{USER_SERVICE_URL}/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    # Fetch orders for the user
    orders = Order.query.filter_by(user_id=user_id).all()

    if not orders:
        return jsonify({"error": "No orders found for this user"}), 404

    return jsonify([order.as_dict() for order in orders]), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
