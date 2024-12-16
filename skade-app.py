from flask import Flask, jsonify, request
import os
import sqlite3
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

DATABASE = "/app/data/skade-database.db"


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