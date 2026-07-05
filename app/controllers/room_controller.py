from flask import jsonify, request
from app.extension import db
from app.models.room import Room

def create_room():
    data = request.get_json()

    new_room = Room(
        room_number=data.get("room_number"),
        room_type=data.get("room_type"),
        capacity=data.get("capacity"),
        is_available=data.get("is_available", True),
        hostel_id=data.get("hostel_id")
    )

    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created successfully", "id": new_room.id}), 201