from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import random
import string

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'license_user'
app.config['MYSQL_PASSWORD'] = 'YourSecurePassword'
app.config['MYSQL_DB'] = 'license_db'
mysql = MySQL(app)

# Function to generate random license keys
def generate_license_key():
    parts = []
    parts.append(''.join(random.choices(string.ascii_uppercase, k=4)))  # ABCD
    parts.append(''.join(random.choices(string.digits, k=4)))  # 1234
    parts.append(''.join(random.choices(string.ascii_lowercase, k=4)))  # efgh
    parts.append(''.join(random.choices(string.punctuation + string.digits + string.ascii_letters, k=6)))  # []{}%$#!

    return '-'.join(parts)

# Route to generate a license key
@app.route('/generate', methods=['POST'])
def generate():
    cursor = mysql.connection.cursor()
    license_key = generate_license_key()

    cursor.execute('INSERT INTO licenses (license_key) VALUES (%s)', (license_key,))
    mysql.connection.commit()

    return jsonify({'license_key': license_key})

# Route to validate a license key
@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    license_key = data.get('license_key')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM licenses WHERE license_key = %s', (license_key,))
    result = cursor.fetchone()

    if result:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)  # Make it accessible externally
