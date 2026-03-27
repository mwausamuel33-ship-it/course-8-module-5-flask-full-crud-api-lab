# Module Lab: Building Full CRUD RESTful APIs with Flask

## Learning Goals

- Implement RESTful API endpoints using Flask.
- Handle HTTP POST, PATCH, and DELETE methods to manage resource data.
- Accept and process JSON input using `request.get_json()`.
- Simulate persistent data using in-memory Python objects.
- Follow RESTful route conventions and return structured JSON responses.

## Introduction

In this lab, you will build a **Full CRUD API** to manage a list of events. The API will allow users to:

- Create new events using `POST /events`
- Update existing events using `PATCH /events/<id>`
- Delete events using `DELETE /events/<id>`

You'll simulate database-like behavior with in-memory Python class objects and respond to all client requests with properly formatted JSON and appropriate status codes.

This lab reinforces essential backend development skills including route design, data mutation, error handling, and RESTful conventions.

## API Overview

The Events API is a simple RESTful service that manages event data in memory. It provides endpoints to create, read, update, and delete events. All responses are returned in JSON format with appropriate HTTP status codes.

### Base URL
```
http://localhost:5000
```

## Setup Instructions

### Fork and Clone the Repository

1. Go to the provided GitHub repository link.
2. Fork the repository to your GitHub account.
3. Clone the forked repository to your local machine:

```bash
git clone <repo-url>
cd course-8-module-5-flask-full-crud-api-lab
```

### Install Dependencies

Ensure Python is installed:

```bash
python --version
```

Install Flask and dependencies using pipenv:

```bash
pipenv install
pipenv shell
```

Or with pip:

```bash
pip install flask
```

## Tasks

### Task 1: Define the Problem

You’re building a basic event management API. It should:

- Accept event creation via `POST /events`
- Allow updating event titles via `PATCH /events/<id>`
- Delete events using `DELETE /events/<id>`
- Respond with structured JSON and appropriate HTTP status codes

---

### Task 2: Determine the Design

The Flask API should be structured as follows:

- Use `@app.route()` with correct HTTP method decorators
- Accept input using `request.get_json()`
- Represent data using a custom `Event` class
- Store events in an in-memory list
- Use `jsonify()` for consistent JSON responses

---

### Task 3: Develop the Code

Create `app.py` and start with the following structure:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# TODO: POST /events - Create a new event from JSON input
# TODO: PATCH /events/<id> - Update the title of an event
# TODO: DELETE /events/<id> - Remove an event from the list

if __name__ == "__main__":
    app.run(debug=True)
```

---

### Task 4: Test the API

Start the Flask development server:

```bash
python app.py
```

The server will run on `http://localhost:5000/`.

---

## API Endpoints

### 1. Create a New Event
**POST** `/events`

Creates a new event and returns it with a generated ID.

**Request:**
```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon"}'
```

**Request Body:**
```json
{
  "title": "Hackathon"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "Hackathon"
}
```

**Error Response (400 Bad Request - Missing Title):**
```json
{
  "error": "Title is required"
}
```

---

### 2. Update an Event
**PATCH** `/events/<id>`

Updates the title of an existing event by ID.

**Request:**
```bash
curl -X PATCH http://localhost:5000/events/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon 2025"}'
```

**Request Body:**
```json
{
  "title": "Hackathon 2025"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Hackathon 2025"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Event not found"
}
```

---

### 3. Delete an Event
**DELETE** `/events/<id>`

Removes an event from the list by ID.

**Request:**
```bash
curl -X DELETE http://localhost:5000/events/2
```

**Response (204 No Content):**
```
(Empty response body)
```

**Error Response (404 Not Found):**
```json
{
  "error": "Event not found"
}
```

---

## Status Codes Reference

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 OK | Success | PATCH request successful |
| 201 Created | Resource created | POST request successful |
| 204 No Content | Success (no body) | DELETE request successful |
| 400 Bad Request | Invalid input | Missing or invalid JSON data |
| 404 Not Found | Resource not found | Event ID doesn't exist |

---

## Best Practices Implemented

✅ **RESTful Route Design**
- Uses nouns in route paths (e.g., `/events` instead of `/getEvents`)
- HTTP methods indicate the action (POST, PATCH, DELETE)

✅ **Input Validation**
- Checks if JSON data is provided
- Validates that required fields (title) are present
- Returns `400 Bad Request` with error message for invalid input

✅ **Proper HTTP Status Codes**
- Returns `201 Created` for successful POST requests
- Returns `200 OK` for successful PATCH requests
- Returns `204 No Content` for successful DELETE requests
- Returns `404 Not Found` when a resource doesn't exist
- Returns `400 Bad Request` for invalid input

✅ **Clear JSON Responses**
- All responses use `jsonify()` for consistent JSON formatting
- Error messages are descriptive and helpful

✅ **Inline Comments**
- Each function and code block includes comments explaining logic
- Comments clarify validation checks and data transformations

✅ **Simple Data Model**
- Uses a custom `Event` class with a `to_dict()` method
- In-memory list simulates a database

---

## Considerations & Future Improvements

**1. Input Validation**
- The API ensures the `title` field is provided before creating or updating events
- Returns clear error messages when validation fails

**2. Event Not Found**
- The API returns `404 Not Found` with a descriptive error message when attempting to access a non-existent event

**3. Unique IDs**
- Event IDs are auto-generated by finding the highest existing ID and incrementing it
- This ensures each event has a unique identifier

**4. Scalability**
- While this implementation uses a single file and in-memory storage, production systems should:
  - Separate concerns into multiple modules (routes, models, services)
  - Use a persistent database (SQLite, PostgreSQL, etc.)
  - Implement authentication and authorization
  - Add rate limiting and caching
  - Use environment variables for configuration

**5. Data Persistence**
- Currently, all data is lost when the server restarts
- For production, integrate a database like SQLAlchemy with Flask

---

## Testing the API

### Using curl

**1. Create an event:**
```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Conference 2025"}'
```

**2. Update an event:**
```bash
curl -X PATCH http://localhost:5000/events/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Annual Conference 2025"}'
```

**3. Delete an event:**
```bash
curl -X DELETE http://localhost:5000/events/2
```

### Using Python requests library

```python
import requests

BASE_URL = "http://localhost:5000"

# Create event
response = requests.post(f"{BASE_URL}/events", json={"title": "Webinar"})
print(response.json())  # {'id': 3, 'title': 'Webinar'}

# Update event
response = requests.patch(f"{BASE_URL}/events/1", json={"title": "Updated Conference"})
print(response.json())  # {'id': 1, 'title': 'Updated Conference'}

# Delete event
response = requests.delete(f"{BASE_URL}/events/2")
print(response.status_code)  # 204
```

### Running the Test Suite

The repository includes automated tests using pytest. Run them with:

```bash
pytest tests/test_app.py -v
```

This will run all test cases and verify:
- Event creation with 201 status code
- Event updates with 200 status code
- Event deletion with 204 status code
- 404 responses for non-existent events

---

## Conclusion

After completing this lab, you will:

✅ Know how to handle incoming JSON with Flask  
✅ Build routes that implement full CRUD behavior  
✅ Simulate persistent resource changes in memory  
✅ Return proper HTTP status codes and structured responses  
✅ Write production-quality code with validation and error handling  
✅ Understand RESTful API design principles  

This is a critical step in your backend developer journey. Next up: persistent databases!
