from flask import jsonify, request
from app.extension import db
from app.models.hostel import Hostel


def create_hostel():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("location"):
        return jsonify({"error": "Name and location are required"}), 400

    new_hostel = Hostel(
        name=data.get("name"),
        location=data.get("location"),
        price_per_bed=data.get("price_per_bed"),
        amenities=data.get("amenities"),
        total_rooms=data.get("total_rooms", 0)
    )
    db.session.add(new_hostel)
    db.session.commit()
    return jsonify({"message": "Hostel created successfully", "id": new_hostel.id}), 201


def get_all_hostels():
    hostels = Hostel.query.all()
    result = []
    for h in hostels:
        result.append({
            "id": h.id,
            "name": h.name,
            "location": h.location,
            "price_per_bed": h.price_per_bed,
            "amenities": h.amenities,
            "total_rooms": h.total_rooms
        })
    return jsonify(result), 200


def get_hostel_by_id(hostel_id):
    hostel = Hostel.query.get(hostel_id)
    if not hostel:
        return jsonify({"error": "Hostel not found"}), 404
    return jsonify({
        "id": hostel.id,
        "name": hostel.name,
        "location": hostel.location,
        "price_per_bed": hostel.price_per_bed,
        "amenities": hostel.amenities,
        "total_rooms": hostel.total_rooms
    }), 200


def update_hostel(hostel_id):
    hostel = Hostel.query.get(hostel_id)
    if not hostel:
        return jsonify({"error": "Hostel not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    hostel.name = data.get("name", hostel.name)
    hostel.location = data.get("location", hostel.location)
    hostel.price_per_bed = data.get("price_per_bed", hostel.price_per_bed)
    hostel.amenities = data.get("amenities", hostel.amenities)
    hostel.total_rooms = data.get("total_rooms", hostel.total_rooms)

    db.session.commit()

    return jsonify({"message": "Hostel updated successfully", "id": hostel.id}), 200


def delete_hostel(hostel_id):
    hostel = Hostel.query.get(hostel_id)
    if not hostel:
        return jsonify({"error": "Hostel not found"}), 404

    db.session.delete(hostel)
    db.session.commit()

    return jsonify({"message": "Hostel deleted successfully"}), 200