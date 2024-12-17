# Skade-Service

Skade-Service is a Flask-based microservice that handles car damage management. It includes endpoints for creating damage reports, retrieving damage details, updating existing entries, and deleting records. The service uses SQLite for database management and provides API documentation via Swagger.

## Features
	•	Create Subscriptions: Add new subscriptions with customer details and terms.
	•	Retrieve Subscriptions: Fetch subscription details by their unique ID.
	•	Update Subscription Status: Change the status of a subscription (e.g., Active, Inactive, Terminated).
	•	Subscription Reporting: Generate reports summarizing active, inactive, and terminated subscriptions.
	•	API Documentation: Integrated Swagger UI for exploring and testing endpoints.

## Requirements

### Python Packages
	•	Python 3.7 or higher
	•	Flask
	•	Flasgger
	•	Python-Dotenv
	•	SQLite (built into Python)

### Python Dependencies

Install the required dependencies using:
```Pip install -r requirements.txt```

### Environment Variables

Create a .env file in the root directory and specify the following:
```FLASK_DEBUG=1```
```DATABASE=skade-database.dbb```

## Getting Started

1. Initialize the Database
The service uses SQLite to store car damage data. The database is automatically initialized when the service starts.
To reinitialize, you can modify the init_db() function in skade.app.py.

2. Start the Service

Run the Flask application:
```python skade.app.py```
The service will be available at: http://127.0.0.1:5005

## API Endpoints

1. GET /

Provides a list of available endpoints in the service.

#### Response Example:
```
{
  "service": "Skade-Service",
  "available_endpoints": [
    {"path": "/create_skade", "method": "POST", "description": "Create a new damage report"},
    {"path": "/get_skade/<int:skade_id>", "method": "GET", "description": "Retrieve a damage report by ID"},
    {"path": "/update_skade/<int:skade_id>", "method": "PUT", "description": "Update an existing damage report"},
    {"path": "/delete_skade/<int:skade_id>", "method": "DELETE", "description": "Delete a damage report by ID"}
  ]
}

```

2. POST /create_subscription

Creates a new damage report.

#### Request Body:
```
{
  "bil_id": 123,
  "stelnummer": "ABC12345DEF67890",
  "beskrivelse": "Ridser på venstre dør",
  "omkostning": 2500.75,
  "forsikringsstatus": "Ikke vurderet",
  "admin_id": 456
}
```

#### Response Example:
```
{
  "message": "Skade oprettet"
}
```

3. GET /get_skade/<int:skade_id>

Retrieves the details of a damage report by its unique ID.

#### Response Example:
```
{
  "skade_id": 1,
  "bil_id": 123,
  "stelnummer": "ABC12345DEF67890",
  "beskrivelse": "Ridser på venstre dør",
  "omkostning": 2500.75,
  "forsikringsstatus": "Ikke vurderet",
  "admin_id": 456
}
```

4. PUT /update_skade/<int:skade_id>

Updates an existing damage report.

#### Request Body:
```
{
  "beskrivelse": "Dybere ridser på venstre dør",
  "omkostning": 3000.00
}
```

#### Response Example:
```
{
  "message": "Skade opdateret"
}
```

5. DELETE /delete_skade/<int:skade_id>

Deletes a damage report by its ID.

#### Response Example:
```
{
  "message": "Skade slettet"
}
```
## Project Structure
```
.
├── skade.app.py           # Main Flask application
├── data/
│   └── skade-database.db  # SQLite database (created automatically)
├── swagger/               # YAML files for API documentation
│   ├── create_skade.yaml
│   ├── get_skade.yaml
│   ├── update_skade.yaml
│   ├── delete_skade.yaml
│   └── home.yaml
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # Project documentation
```

## Development Notes

### Swagger Documentation
	•	Swagger is available at /apidocs.
	•	API specifications are written in YAML and stored in the swagger/ folder.

### Database Management
####	•	Initialization: Automatically initializes the database on start.
####	•	Schema:
	•	skade_id: Unique ID for damage entry (primary key).
	•	bil_id: Car ID (foreign key).
	•	stelnummer: Car chassis number.
	•	beskrivelse: Description of the damage.
	•	omkostning: Cost of the repair.
	•	forsikringsstatus: Insurance status (e.g., "Ikke vurderet").
	•	admin_id: Administrator ID.

## Contributions

Feel free to fork the repository and submit pull requests. For major changes, open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License. See LICENSE for more information.
