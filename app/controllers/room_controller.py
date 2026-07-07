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


def get_all_rooms():
    rooms = Room.query.all()
    result = []
    for r in rooms:
        result.append({
            "id": r.id,
            "room_number": r.room_number,
            "room_type": r.room_type,
            "capacity": r.capacity,
            "is_available": r.is_available,
            "hostel_id": r.hostel_id
        })
    return jsonify(result), 200


def get_room_by_id(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify({
        "id": room.id,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "capacity": room.capacity,
        "is_available": room.is_available,
        "hostel_id": room.hostel_id
    }), 200


def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    data = request.get_json()
    room.room_number = data.get("room_number", room.room_number)
    room.room_type = data.get("room_type", room.room_type)
    room.capacity = data.get("capacity", room.capacity)
    room.is_available = data.get("is_available", room.is_available)
    room.hostel_id = data.get("hostel_id", room.hostel_id)

    db.session.commit()

    return jsonify({"message": "Room updated successfully", "id": room.id}), 200