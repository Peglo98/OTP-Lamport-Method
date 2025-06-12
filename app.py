from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__)

# In-memory user store: { username: { 'hash': current_hash, 'uses': remaining_uses } }
user_store = {}

def hash_n(password: str, n: int) -> str:
    """
    Compute H^n(password) using SHA-256.
    """
    h = password.encode('utf-8')
    for _ in range(n):
        h = hashlib.sha256(h).hexdigest().encode('utf-8')
    return h.decode('utf-8')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    n = data.get('n', 5)

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if username in user_store:
        return jsonify({'error': 'User already exists'}), 400

    # Compute the initial hash H^n(P)
    initial_hash = hash_n(password, n)

    # Generate the full OTP chain: [H^(n-1)(P), H^(n-2)(P), ..., H^0(P)]
    otps = [hash_n(password, i - 1) for i in range(n, 0, -1)]

    # Store user record with initial hash and remaining uses
    user_store[username] = {
        'hash': initial_hash,
        'uses': n
    }

    return jsonify({
        'message': 'Registration successful',
        'remaining_uses': n,
        'otps': otps
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    otp = data.get('otp')

    if not username or not otp:
        return jsonify({'error': 'Username and OTP required'}), 400
    if username not in user_store:
        return jsonify({'error': 'User not found. Please register.'}), 404

    record = user_store[username]
    expected_hash = record['hash']

    # Verify: H(OTP) should equal stored hash
    otp_hash = hashlib.sha256(otp.encode('utf-8')).hexdigest()
    if otp_hash != expected_hash:
        return jsonify({'error': 'Invalid OTP'}), 401

    # Successful login: update hash and decrement uses
    record['hash'] = otp  # next expected hash
    record['uses'] -= 1

    if record['uses'] <= 0:
        # No more OTPs left; require re-registration
        del user_store[username]
        return jsonify({'message': 'Login successful, but OTP chain exhausted. Please register again.'}), 200

    return jsonify({
        'message': 'Login successful',
        'remaining_uses': record['uses']
    }), 200

@app.route('/status/<username>', methods=['GET'])
def status(username):
    """Check remaining OTP uses for a user."""
    if username not in user_store:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'remaining_uses': user_store[username]['uses']}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)