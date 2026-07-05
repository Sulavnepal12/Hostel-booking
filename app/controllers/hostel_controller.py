from flask import jsonify, request
from app.extension import db
from app.models.hostel import Hostel

def create_hostel():
    data = request.get_json()

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