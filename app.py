from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# List of events
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# POST route to create a new event
@app.route("/events", methods=["POST"])
def create_event():
    # Get the data from the request
    data = request.get_json()
    
    # Check if data exists and has a title
    if data is None:
        return jsonify({"error": "Title is required"}), 400
    
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Find the highest ID
    highest_id = 0
    for event in events:
        if event.id > highest_id:
            highest_id = event.id
    
    # Create new ID
    new_id = highest_id + 1
    
    # Create the new event
    new_event = Event(new_id, data["title"])
    
    # Add it to the list
    events.append(new_event)
    
    # Return the event data
    return jsonify(new_event.to_dict()), 201

# PATCH route to update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Find the event in the list
    found_event = None
    for event in events:
        if event.id == event_id:
            found_event = event
            break
    
    # Check if event was found
    if found_event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Get the data from the request
    data = request.get_json()
    
    # Check if data exists and has a title
    if data is None:
        return jsonify({"error": "Title is required"}), 400
    
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Update the title
    found_event.title = data["title"]
    
    # Return the updated event
    return jsonify(found_event.to_dict()), 200

# DELETE route to remove an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event in the list
    found_event = None
    for event in events:
        if event.id == event_id:
            found_event = event
            break
    
    # Check if event was found
    if found_event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Remove the event from the list
    events.remove(found_event)
    
    # Return empty response
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
