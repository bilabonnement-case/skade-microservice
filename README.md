# skade-microservice
# Skade-Service

**Skade-Service** er en Flask-baseret microservice, der håndterer registrering, opdatering og sletning af skader på biler. Tjenesten understøtter CRUD-operationer og har integreret Swagger-dokumentation for API-endepunkterne.

---

## Features

- **Opret Skade**: Opret nye skader for biler.
- **Hent Skade**: Hent detaljer om en skade baseret på skade-ID.
- **Opdater Skade**: Opdater oplysninger for en eksisterende skade.
- **Slet Skade**: Slet en registreret skade.
- **API Dokumentation**: Swagger UI er integreret for test og udforskning af API-endepunkter.

---

## Requirements

### Python Packages
- **Python** 3.7 eller højere
- **Flask**
- **Flask-Swagger** (Flasgger)
- **python-dotenv**
- **Flask-Cors**

### Dependencies
Installer nødvendige afhængigheder ved at køre:
```bash
pip install -r requirements.txt
Environment Variables
Opret en .env-fil i roden af projektet og angiv følgende variabler:

plaintext
Copy code
FLASK_DEBUG=1
DATABASE=/app/data/skade-database.db
Getting Started
Initialiser Databasen
Skade-Service bruger SQLite som database. Tabellen skader initialiseres automatisk ved opstart.

Hvis databasen skal reinitialiseres, kan du justere init_db() funktionen i skade.app.py.

Start Servicen
Kør Flask-applikationen med følgende kommando:

bash
Copy code
python skade.app.py
Servicen vil være tilgængelig på: http://127.0.0.1:5005

API Endpoints
GET /
Returnerer en liste over tilgængelige endepunkter.

Respons Eksempel:

json
Copy code
{
  "service": "Skade-Service",
  "endpoints": [
    {"path": "/create_skade", "method": "POST", "description": "Create a new damage report"},
    {"path": "/get_skade/<int:skade_id>", "method": "GET", "description": "Retrieve a damage report by ID"},
    {"path": "/update_skade/<int:skade_id>", "method": "PUT", "description": "Update an existing damage report"},
    {"path": "/delete_skade/<int:skade_id>", "method": "DELETE", "description": "Delete a damage report by ID"}
  ]
}
POST /create_skade
Beskrivelse: Opretter en ny skaderegistrering.

Request Body:

json
Copy code
{
  "bil_id": 123,
  "stelnummer": "ABC12345DEF67890",
  "beskrivelse": "Ridser på venstre dør",
  "omkostning": 2500.75,
  "forsikringsstatus": "Ikke vurderet",
  "admin_id": 456
}
Respons Eksempel:

json
Copy code
{
  "message": "Skade oprettet"
}
GET /get_skade/<int:skade_id>
Beskrivelse: Henter detaljer om en specifik skade.

Respons Eksempel:

json
Copy code
{
  "skade_id": 1,
  "bil_id": 123,
  "stelnummer": "ABC12345DEF67890",
  "beskrivelse": "Ridser på venstre dør",
  "omkostning": 2500.75,
  "forsikringsstatus": "Ikke vurderet",
  "admin_id": 456
}
PUT /update_skade/<int:skade_id>
Beskrivelse: Opdaterer en eksisterende skade.

Request Body:

json
Copy code
{
  "beskrivelse": "Dybe ridser på venstre dør",
  "omkostning": 3000.00
}
Respons Eksempel:

json
Copy code
{
  "message": "Skade opdateret"
}
DELETE /delete_skade/<int:skade_id>
Beskrivelse: Sletter en skade baseret på skade-ID.

Respons Eksempel:

json
Copy code
{
  "message": "Skade slettet"
}
Projektstruktur
plaintext
Copy code
.
├── skade.app.py           # Hoved-Flask applikation
├── data/
│   └── skade-database.db  # SQLite database
├── swagger/               # YAML filer for Swagger-dokumentation
│   ├── home.yaml
│   ├── create_skade.yaml
│   ├── get_skade.yaml
│   ├── update_skade.yaml
│   └── delete_skade.yaml
├── requirements.txt       # Projektets afhængigheder
├── .env                   # Miljøvariabler
└── README.md              # Dokumentation
Swagger Dokumentation
Swagger UI er tilgængelig på /apidocs.
YAML-specifikationerne for API'et findes i swagger/-mappen.
Contributions
Fork gerne dette repository og opret en pull request. For større ændringer, åbn en issue for at diskutere ændringerne.

License
Dette projekt er licenseret under MIT License. Se LICENSE for mere information.
