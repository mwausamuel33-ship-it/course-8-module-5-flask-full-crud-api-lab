from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    """
    Represents an event with an ID and title.
    
    The to_dict() method converts the object to a JSON-serializable dictionary.
    This pattern makes it easy to return event data to API clients.
    """
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# List of events (in-memory data store)
# Note: In a production system, this would be a database (SQLite, PostgreSQL, etc.)
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# ============================================================================
# HELPER FUNCTION
# ============================================================================
# Challenge: Searching for an event by ID was repeated in multiple routes.
# Solution: Extract into a helper function to reduce duplicate code.
# Trade-off: Adds an extra function, but makes code more maintainable and testable.
# ============================================================================

def find_event_by_id(event_id):
    """
    Helper function to find an event by ID.
    
    This function encapsulates the search logic used in multiple routes.
    If the application grows, this could be moved to a separate service layer.
    
    Args:
        event_id: The ID of the event to find
        
    Returns:
        The Event object if found, or None if not found
    """
    for event in events:
        if event.id == event_id:
            return event
    return None

# ============================================================================
# INPUT VALIDATION HELPER
# ============================================================================

def validate_json_data(data):
    """
    Validates that JSON data exists and contains required fields.
    
    Challenge: Multiple routes need to validate the same data structure.
    Solution: Centralize validation logic in a helper function.
    
    Args:
        data: The JSON data from request.get_json()
        
    Returns:
        A tuple of (is_valid, error_message)
    """
    if data is None:
        return False, "No JSON data provided"
    
    if "title" not in data:
        return False, "Title is required"
    
    return True, None

# ============================================================================
# ROUTES
# ============================================================================

# Welcome route - GET /
@app.route("/", methods=["GET"])
def welcome():
    """
    Welcome route that returns a JSON message.
    
    This endpoint serves as the root of the API and provides a simple
    JSON response to confirm the API is running.
    
    Returns:
        A JSON object with a welcome message and status code 200
    """
    return jsonify({
        "message": "Welcome to the Events API",
        "description": "A simple CRUD API for managing events",
        "endpoints": {
            "GET /": "Welcome message",
            "GET /events": "List all events",
            "POST /events": "Create a new event",
            "PATCH /events/<id>": "Update an event",
            "DELETE /events/<id>": "Delete an event"
        }
    }), 200

# GET route to list all events
@app.route("/events", methods=["GET"])
def get_events():
    """
    Returns a list of all events.
    
    This endpoint retrieves all events from the in-memory data store
    and returns them as a JSON array.
    
    Returns:
        A JSON array of event objects with status code 200
    """
    # Convert all events to dictionaries
    events_list = [event.to_dict() for event in events]
    
    # Return the list of events
    return jsonify(events_list), 200

# POST route to create a new event
@app.route("/events", methods=["POST"])
def create_event():
    """
    Creates a new event.
    
    Challenge: What if the user submits no data or misses the title field?
    Solution: Validate the JSON data and return a 400 error if invalid.
    Trade-off: Adds validation logic, but protects the API from bad data.
    """
    # Get the data from the request
    data = request.get_json()
    
    # Validate the incoming data
    is_valid, error_message = validate_json_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Find the highest ID to generate a new one
    highest_id = 0
    for event in events:
        if event.id > highest_id:
            highest_id = event.id
    
    new_id = highest_id + 1
    
    # Create and store the new event
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    # Return the created event with 201 Created status
    return jsonify(new_event.to_dict()), 201

# PATCH route to update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """
    Updates an existing event's title.
    
    Challenge: What happens if the event ID doesn't exist?
    Solution: Search for the event and return 404 with a clear message if not found.
    Trade-off: Adds a conditional check, but greatly improves frontend usability.
    """
    # Use the helper function to find the event
    event = find_event_by_id(event_id)
    
    # Return 404 if not found
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Validate the incoming data
    data = request.get_json()
    is_valid, error_message = validate_json_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Update the event title
    event.title = data["title"]
    
    # Return the updated event with 200 OK status
    return jsonify(event.to_dict()), 200

# DELETE route to remove an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Deletes an event from the list.
    
    Challenge: What if someone tries to delete an event that doesn't exist?
    Solution: Check if the event exists before removing it.
    Trade-off: Adds a lookup step, but prevents silent failures.
    """
    # Use the helper function to find the event
    event = find_event_by_id(event_id)
    
    # Return 404 if not found
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Remove the event from the list
    events.remove(event)
    
    # Return 204 No Content (successful deletion, no body needed)
    return "", 204

# ============================================================================
# SCALABILITY NOTE
# ============================================================================
# Challenge: A single file with all logic won't scale as the application grows.
# Solution: As features are added, consider restructuring:
#   - routes/: Separate route files for different resources
#   - models/: Event class and other data models
#   - services/: Business logic (event lookup, validation, etc.)
#   - database/: Database models and queries (future)
#
# This will make the codebase more maintainable and testable.
# ============================================================================

if __name__ == "__main__":
    app.run(debug=True)
