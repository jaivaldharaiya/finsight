import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import os

# --- APP CONFIGURATION ---
app = Flask(__name__)
CORS(app)  # This will allow your Vue app to talk to this server

# --- DATABASE CONFIGURATION ---
DATABASE = 'finsight.db'

# --- SECURITY CONFIGURATION ---
# IMPORTANT: Change this secret key in a real production environment!
app.config["JWT_SECRET_KEY"] = "your-super-secret-key-for-finsight-hackathon"
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# --- DATABASE HELPER FUNCTIONS ---

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    # This allows you to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    if os.path.exists(DATABASE):
        return  # Database already exists
    
    print("Creating database...")
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()
    print("Database created successfully.")

# --- API ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    """Handles new user registration."""
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'phone', 'password')):
        return jsonify({"error": "Missing required fields"}), 400

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    # Hash the password for security
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO users (name, email, phone, password_hash) VALUES (?, ?, ?, ?)',
            (name, email, phone, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Phone number or email already exists"}), 409 # 409 Conflict
    finally:
        conn.close()
        
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    """Handles user login and returns a JWT."""
    data = request.get_json()
    if not data or not all(k in data for k in ('phone', 'password')):
        return jsonify({"error": "Missing phone or password"}), 400
        
    phone = data.get('phone')
    password = data.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE phone = ?', (phone,)).fetchone()
    conn.close()
    
    # Check if user exists and if the password is correct
    if user and bcrypt.check_password_hash(user['password_hash'], password):
        # Create a new token with the user's ID as the identity
        access_token = create_access_token(identity=user['id'])
        return jsonify(access_token=access_token)

    return jsonify({"error": "Invalid phone number or password"}), 401


# --- EXAMPLE PROTECTED ROUTE ---
@app.route('/api/profile', methods=['GET'])
@jwt_required() # This decorator protects the route
def get_profile():
    """An example of a route that requires a valid JWT."""
    current_user_id = get_jwt_identity() # Get the user ID from the token
    
    conn = get_db_connection()
    user = conn.execute('SELECT id, name, email, phone FROM users WHERE id = ?', (current_user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify(dict(user))


# --- MAIN EXECUTION BLOCK ---
if __name__ == '__main__':
    init_db()  # Initialize the database on first run
    app.run(host='0.0.0.0', port=9000, debug=True)
