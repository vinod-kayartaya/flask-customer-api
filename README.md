# Flask Customer API

A RESTful API for managing customer information built with Flask and SQLite.

## Features

- CRUD operations for customer management
- Input validation
- Unique email and phone constraints
- SQLite database persistence
- Unit tests
- Multi-tiered architecture (Controller -> Service -> DAO)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   └── customer_controller.py
│   ├── dao/
│   │   └── customer_dao.py
│   ├── dto/
│   │   └── customer_dto.py
│   ├── models/
│   │   └── customer.py
│   └── services/
│       └── customer_service.py
├── tests/
│   └── test_customer_api.py
├── requirements.txt
├── run.py
└── README.md
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

- `POST /api/customers` - Create a new customer
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get a specific customer
- `PUT /api/customers/<id>` - Update a customer
- `DELETE /api/customers/<id>` - Delete a customer

## Running Tests

```bash
python -m unittest tests/test_customer_api.py
```

## Customer Model

- `id`: Auto-generated integer (primary key)
- `name`: String (required)
- `email`: String (required, unique)
- `phone`: String (optional, unique)
- `city`: String (optional)
