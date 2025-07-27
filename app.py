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
    conn = get_db_connection()
    
    # Check if users table exists
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Creating users table...")
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
        print("Users table created successfully.")
    else:
        print("Database already initialized.")
    
    conn.close()

# --- API ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    """Handles new user registration."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'phone', 'password')):
            return jsonify({"error": "Missing required fields"}), 400

        name = data.get('name').strip()
        email = data.get('email').strip().lower()
        phone = data.get('phone').strip()
        password = data.get('password')

        # Basic validation
        if not name or not email or not phone or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Hash the password for security
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (name, email, phone, password_hash) VALUES (?, ?, ?, ?)',
                (name, email, phone, password_hash)
            )
            conn.commit()
            print(f"User registered successfully: {name} ({phone})")
        except sqlite3.IntegrityError as e:
            conn.close()
            if 'phone' in str(e):
                return jsonify({"error": "Phone number already exists"}), 409
            elif 'email' in str(e):
                return jsonify({"error": "Email already exists"}), 409
            else:
                return jsonify({"error": "Registration failed"}), 409
        finally:
            conn.close()
            
        return jsonify({"message": "User registered successfully"}), 201
    
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Handles user login and returns a JWT."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('phone', 'password')):
            return jsonify({"error": "Missing phone or password"}), 400
            
        phone = data.get('phone').strip()
        password = data.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE phone = ?', (phone,)).fetchone()
        conn.close()
        
        # Check if user exists and if the password is correct
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            # Create a new token with the user's ID as the identity
            access_token = create_access_token(identity=user['id'])
            print(f"User logged in successfully: {phone}")
            return jsonify(access_token=access_token)

        print(f"Login failed for phone: {phone}")
        return jsonify({"error": "Invalid phone number or password"}), 401
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


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
    app.run(host='0.0.0.0', port=5000, debug=True)
