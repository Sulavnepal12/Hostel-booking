from flask import jsonify, request, session
from app.extension import db
from app.models.booking import Booking
from app.models.room import Room
from datetime import datetime


def create_booking():
    data = request.get_json()

    if not data or not data.get("guest_name") or not data.get("room_id"):
        return jsonify({"error": "Guest name and room_id are required"}), 400

    try:
        check_in = datetime.strptime(data.get("check_in"), "%Y-%m-%d").date()
        check_out = datetime.strptime(data.get("check_out"), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    room = Room.query.get(data.get("room_id"))
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if not room.is_available:
        return jsonify({"error": "Room is not available"}), 400

    new_booking = Booking(
        guest_name=data.get("guest_name"),
        guest_email=data.get("guest_email"),
        check_in=check_in,
        check_out=check_out,
        status="pending",
        room_id=data.get("room_id"),
        user_id=session.get("user_id")
    )

    room.is_available = False

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking created successfully", "id": new_booking.id}), 201


def get_all_bookings():
    bookings = Booking.query.all()
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "guest_name": b.guest_name,
            "guest_email": b.guest_email,
            "check_in": b.check_in.isoformat(),
            "check_out": b.check_out.isoformat(),
            "status": b.status,
            "room_id": b.room_id,
            "user_id": b.user_id
        })
    return jsonify(result), 200


def get_my_bookings():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    bookings = Booking.query.filter_by(user_id=session.get("user_id")).all()
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "guest_name": b.guest_name,
            "guest_email": b.guest_email,
            "check_in": b.check_in.isoformat(),
            "check_out": b.check_out.isoformat(),
            "status": b.status,
            "room_id": b.room_id
        })
    return jsonify(result), 200


def get_booking_by_id(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({
        "id": booking.id,
        "guest_name": booking.guest_name,
        "guest_email": booking.guest_email,
        "check_in": booking.check_in.isoformat(),
        "check_out": booking.check_out.isoformat(),
        "status": booking.status,
        "room_id": booking.room_id,
        "user_id": booking.user_id
    }), 200


def update_booking_status(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["pending", "confirmed", "cancelled"]:
        return jsonify({"error": "Invalid status value"}), 400

    booking.status = new_status
    db.session.commit()

    return jsonify({"message": "Booking status updated successfully", "status": booking.status}), 200


def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    booking.status = "cancelled"

    room = Room.query.get(booking.room_id)
    if room:
        room.is_available = True

    db.session.commit()

    return jsonify({"message": "Booking cancelled successfully"}), 200