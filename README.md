# Events API - A Simple CRUD Project

## What is this?

I built a simple API that manages events. You can create, read, update, and delete events. It's a great way to learn how REST APIs work!

## What I learned

- How to use Flask to make a web API
- How to use different HTTP methods (GET, POST, PATCH, DELETE)
- How to handle JSON data
- How to return proper status codes (200, 201, 404, etc.)
- How to validate user input

## How to set it up

### 1. Get the code

```bash
git clone <repo-url>
cd course-8-module-5-flask-full-crud-api-lab
```

### 2. Install stuff

You need Flask installed. If you have pip:

```bash
pip install flask pytest
```

Or use pipenv:

```bash
pipenv install
pipenv shell
```

### 3. Run the app

```bash
python app.py
```

Now go to `http://localhost:5000` in your browser!

## The API endpoints

### GET / - Welcome message

Shows info about the API.

```bash
curl http://localhost:5000/
```

Response:
```json
{
  "message": "Welcome to the Events API",
  "description": "A simple CRUD API for managing events",
  "endpoints": { ... }
}
```

### GET /events - List all events

Gets all the events from the list.

```bash
curl http://localhost:5000/events
```

Response:
```json
[
  {"id": 1, "title": "Tech Meetup"},
  {"id": 2, "title": "Python Workshop"}
]
```

### POST /events - Create a new event

Make a new event. You have to send a title in the JSON.

```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon"}'
```

Request:
```json
{"title": "Hackathon"}
```

Response (201 Created):
```json
{"id": 3, "title": "Hackathon"}
```

If you forget the title, you get a 400 error:
```json
{"error": "Title is required"}
```

### PATCH /events/<id> - Update an event

Changes the title of an event.

```bash
curl -X PATCH http://localhost:5000/events/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

Response (200 OK):
```json
{"id": 1, "title": "Updated Title"}
```

If the event doesn't exist, you get a 404:
```json
{"error": "Event not found"}
```

### DELETE /events/<id> - Delete an event

Removes an event from the list.

```bash
curl -X DELETE http://localhost:5000/events/2
```

Response: 204 No Content (no data, just success)

If it doesn't exist:
```json
{"error": "Event not found"}
```

## Status codes I used

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Update worked |
| 201 | Created | New event made |
| 204 | No Content | Delete worked |
| 400 | Bad Request | Missing title or bad JSON |
| 404 | Not Found | Event doesn't exist |

## How the code works

### The Event class

Simple class that has an id and title. The `to_dict()` method turns it into a dictionary so we can send it as JSON.

### The events list

This is like a mini database. It's just a list in memory. When the app restarts, all the data goes away. In a real app, we'd use a real database.

### Helper functions

I made two helper functions:
- `find_event_by_id()` - searches for an event by ID instead of writing this code over and over
- `validate_json_data()` - checks if the data the user sent is valid

### Validation

Before creating or updating, I check:
- Is there any data?
- Does it have a "title" field?

If anything is wrong, I return a 400 error with a message.

### Finding events

I loop through the events list and check the IDs. If I find it, I return it. If not, I return None.

### Returning data

Everything comes back as JSON. I use `jsonify()` to convert Python stuff to JSON. And I return the right status code (201 for created, 200 for ok, 404 for not found, etc.)

## Testing

Run the tests with:

```bash
pytest tests/test_app.py -v
```

This runs all the tests and makes sure everything works right.

## Things I want to improve

- Right now data is stored in memory, so it disappears when you restart. A database would be better.
- I could add more features like searching or filtering events
- I could add authentication so only certain people can create/delete events
- I could split the code into multiple files as it gets bigger
- Maybe add a frontend to make it easier to use?

## Cool things I learned

- Flask makes it super easy to make an API
- Status codes matter! They tell the client what happened
- Validation is important so people can't send bad data
- Helper functions reduce code duplication
- The `jsonify()` function is useful for returning JSON

Good luck with the API! Feel free to play around with it!
