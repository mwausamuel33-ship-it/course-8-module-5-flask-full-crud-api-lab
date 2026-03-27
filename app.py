from flask import Flask, jsonify, request

app = Flask(__name__)

# simple event class - has an id and title
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        # converts the event to a dictionary so we can return it as JSON
        return {"id": self.id, "title": self.title}

# list of events - this is like our "database" for now
# when the app restarts, we lose all the data... but that's ok for now
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# helper function to find events by id
# i was repeating this code a lot so i made it a function
def find_event_by_id(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# helper to validate the incoming JSON
def validate_json_data(data):
    if data is None:
        return False, "No JSON data provided"
    
    if "title" not in data:
        return False, "Title is required"
    
    return True, None

# welcome route - returns info about the api
@app.route("/", methods=["GET"])
def welcome():
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

# get all events
@app.route("/events", methods=["GET"])
def get_events():
    # loop through all events and convert them to dictionaries
    events_list = [event.to_dict() for event in events]
    return jsonify(events_list), 200

# create a new event
@app.route("/events", methods=["POST"])
def create_event():
    # get the json data from the request
    data = request.get_json()
    
    # check if the data is valid
    is_valid, error_message = validate_json_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # find the highest id so we can make a new id
    highest_id = 0
    for event in events:
        if event.id > highest_id:
            highest_id = event.id
    
    new_id = highest_id + 1
    
    # create the event and add it to the list
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    # return the new event with status 201 (created)
    return jsonify(new_event.to_dict()), 201

# update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # find the event
    event = find_event_by_id(event_id)
    
    # if we can't find it, return 404
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # get the json data
    data = request.get_json()
    
    # validate it
    is_valid, error_message = validate_json_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # update the title
    event.title = data["title"]
    
    # return the updated event
    return jsonify(event.to_dict()), 200

# delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # find the event
    event = find_event_by_id(event_id)
    
    # if not found, return 404
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # remove it from the list
    events.remove(event)
    
    # return 204 (no content) because we deleted it
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
