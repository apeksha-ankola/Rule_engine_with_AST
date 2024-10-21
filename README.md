# Rule Engine with Abstract Syntax Tree (AST)

A Python-based Rule Engine that allows for the creation, evaluation, and management of conditional rules using Abstract Syntax Trees (AST). The engine supports storing rules in a SQLite database and provides a Flask API for rule management.

## Features

- Create and evaluate rules based on user-defined conditions.
- Supports conditional rules using AST for eligibility determination.
- API endpoints for rule creation, evaluation, and management.
- SQLite database for storing rules and AST structures.
- Comprehensive error handling and validation mechanisms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Pip (Python package installer) installed.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/apeksha-ankola/Rule_engine_with_AST.git
   cd Rule_engine_with_AST
   
2. Create a virtual environment. This is optional but recommended:
   ```
   python -m venv venv
   source venv/bin/activate
   # On Windows use `venv\Scripts\activate`
   
   ```
  
4. Install the required packages:
   ```
   pip install -r requirements.txt
   
   ```

6. Initialize the SQLite database:
   ```
   python database.py
   ```
7. Run the application
  ```
  python app.py
  ```
The API will be available at http://127.0.0.1:5000.


## API Endpoints
1. Create a Rule
Endpoint: POST/create_rule
Request Body: 
```
{
    "rule": "age > 18 AND income < 50000"
}

```
2. Evaluate a Rule
Endpoint: POST/evaluate_rule
Request Body:

```
{
    "rule_id": 1,
    "context": {
        "age": 20,
        "income": 40000
    }
}
```
3. Get All Rules
Endpoint: GET /rules

5. Delete a Rule
Endpoint: DELETE /delete_rule/{rule_id}


## Testing
To run the tests, execute the following command:

```
pytest test.py

```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Notes:
- Update the API endpoints with actual request/response formats based on your implementation.
- If you have specific instructions for the database or additional dependencies, include them in the Installation section.
- Adjust the Contributing and License sections according to your preferences.






