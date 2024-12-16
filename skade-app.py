from flask import Flask, jsonify, request
import os
import sqlite3
import requests  # Til validering af bil_id og admin_id via HTTP-kald
from dotenv import load_dotenv
from flasgger import Swagger, swag_from

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'Skade Microservice API',
    'uiversion': 3,
    'openapi': '3.0.0'
}
swagger = Swagger(app)

DATABASE = "skade-database.db"

BIL_SERVICE_URL = os.getenv("BIL_SERVICE_URL", "http://localhost:5003")  # URL til Bil-microservice
ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL", "http://localhost:5002")  # URL til Admin-microservice

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skader (
            skade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bil_id INTEGER NOT NULL,
            stelnummer TEXT NOT NULL,
            beskrivelse TEXT,
            omkostning REAL,
            forsikringsstatus TEXT,
            admin_id INTEGER NOT NULL,
            FOREIGN KEY (bil_id) REFERENCES bil(bil_id),
            FOREIGN KEY (admin_id) REFERENCES admin(admin_id)
        )
        """)
        conn.commit()

init_db()


# Helper: Valider bil_id via Bil-microservice
def validate_bil_id(bil_id):
    response = requests.get(f"{BIL_SERVICE_URL}/get_bil/{bil_id}")
    return response.status_code == 200

# Helper: Valider admin_id via Admin-microservice
def validate_admin_id(admin_id):
    response = requests.get(f"{ADMIN_SERVICE_URL}/get_admin/{admin_id}")
    return response.status_code == 200

# Home
@app.route('/')
@swag_from('swagger/home.yaml')
def home():
    return jsonify({
        "service": "Skade-Service",
        "endpoints": [
            {"path": "/create_skade", "method": "POST"},
            {"path": "/get_skade/<int:skade_id>", "method": "GET"},
            {"path": "/update_skade/<int:skade_id>", "method": "PUT"},
            {"path": "/delete_skade/<int:skade_id>", "method": "DELETE"},
        ]
    })

# create_skade
@app.route('/create_skade', methods=['POST'])
@swag_from('swagger/create_skade.yaml')
def create_skade():
    data = request.get_json()

    bil_id = data['bil_id']
    stelnummer = data['stelnummer']
    beskrivelse = data.get('beskrivelse', "")
    omkostning = data.get('omkostning', 0.0)
    forsikringsstatus = data.get('forsikringsstatus', "Ikke vurderet")
    admin_id = data['admin_id']

    # Valider bil_id og admin_id
    if not validate_bil_id(bil_id):
        return jsonify({"error": "Invalid bil_id"}), 400
    if not validate_admin_id(admin_id):
        return jsonify({"error": "Invalid admin_id"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO skader (bil_id, stelnummer, beskrivelse, omkostning, forsikringsstatus, admin_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (bil_id, stelnummer, beskrivelse, omkostning, forsikringsstatus, admin_id))
        conn.commit()

    return jsonify({"message": "Skade oprettet"}), 201

# get_skade
@app.route('/get_skade/<int:skade_id>', methods=['GET'])
@swag_from('swagger/get_skade.yaml')
def get_skade(skade_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM skader WHERE skade_id = ?", (skade_id,))
        skade = cursor.fetchone()

    if skade:
        keys = ['skade_id', 'bil_id', 'stelnummer', 'beskrivelse', 'omkostning', 'forsikringsstatus', 'admin_id']
        return jsonify(dict(zip(keys, skade))), 200

    return jsonify({"error": "Skade ikke fundet"}), 404

# update_skade
@app.route('/update_skade/<int:skade_id>', methods=['PUT'])
@swag_from('swagger/update_skade.yaml')
def update_skade(skade_id):
    data = request.get_json()
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} = ?")
        values.append(value)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE skader SET {', '.join(fields)} WHERE skade_id = ?", (*values, skade_id))
        conn.commit()

    return jsonify({"message": "Skade opdateret"}), 200

# delete_skade
@app.route('/delete_skade/<int:skade_id>', methods=['DELETE'])
@swag_from('swagger/delete_skade.yaml')
def delete_skade(skade_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skader WHERE skade_id = ?", (skade_id,))
        conn.commit()

    return jsonify({"message": "Skade slettet"}), 200

if __name__ == '__main__':
    app.run(debug=bool(int(os.getenv('FLASK_DEBUG', 0))), host='0.0.0.0', port=5005)