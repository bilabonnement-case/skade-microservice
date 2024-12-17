Skade-Service
Skade-Service er en Flask-baseret microservice, der håndterer registrering, opdatering og sletning af skader på biler. Tjenesten understøtter CRUD-operationer og har integreret Swagger-dokumentation for API-endepunkter.

Features
Opret Skade: Opretter nye skader for biler.
Hent Skade: Henter detaljer for en given skade ved ID.
Opdater Skade: Opdaterer oplysninger om en eksisterende skade.
Slet Skade: Sletter en registreret skade.
Swagger Dokumentation: Swagger UI til udforskning og test af API.
Krav
Python Krav
Python 3.7 eller højere
Flask
Flask-Swagger (Flasgger)
python-dotenv
Flask-Cors
Installation af Dependencies
Installer nødvendige afhængigheder ved at køre:

bash
Copy code
pip install -r requirements.txt
Environment Variables
Opret en .env-fil i roden af projektet og angiv følgende miljøvariabler:

plaintext
Copy code
FLASK_DEBUG=1
DATABASE=/app/data/skade-database.db
Projektstruktur
Følgende projektstruktur anvendes:

plaintext
Copy code
.
├── skade.app.py           # Hoved Flask-applikation
├── data/
│   └── skade-database.db  # SQLite database
├── swagger/               # YAML-filer til Swagger
│   ├── home.yaml
│   ├── create_skade.yaml
│   ├── get_skade.yaml
│   ├── update_skade.yaml
│   └── delete_skade.yaml
├── requirements.txt       # Afhængigheder
├── .env                   # Miljøvariabler
└── README.md              # Dokumentation
Sådan Startes Servicen
Initialisering af Databasen
Databasen skade-database.db initialiseres automatisk, når applikationen startes.

Start Flask-Applikationen
Kør applikationen med:

bash
Copy code
python skade.app.py
Servicen er tilgængelig på: http://127.0.0.1:5005

API Endpoints
GET /
Beskrivelse: Returnerer en liste over alle tilgængelige endepunkter i servicen.

Respons:

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
Respons:

json
Copy code
{
  "message": "Skade oprettet"
}
GET /get_skade/<int:skade_id>
Beskrivelse: Henter detaljer for en specifik skade.

Respons:

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
Beskrivelse: Opdaterer oplysninger for en eksisterende skade.

Request Body:

json
Copy code
{
  "beskrivelse": "Dybe ridser på venstre dør",
  "omkostning": 3000.00
}
Respons:

json
Copy code
{
  "message": "Skade opdateret"
}
DELETE /delete_skade/<int:skade_id>
Beskrivelse: Sletter en skade ved det givne ID.

Respons:

json
Copy code
{
  "message": "Skade slettet"
}
Swagger Dokumentation
Swagger UI er tilgængelig på /apidocs.
API-specifikationerne findes som YAML-filer i swagger/-mappen.

Bidrag
Du er velkommen til at fork'e repository'et og indsende pull requests. For større ændringer, åbn en issue først for at diskutere ændringerne.

Licens
Dette projekt er licenseret under MIT License. Se LICENSE for detaljer.
