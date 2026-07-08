from flask import Blueprint
from app.controllers.hostel_controller import create_hostel, get_all_hostels, get_hostel_by_id, update_hostel, delete_hostel
from app.controllers.room_controller import create_room, get_all_rooms, get_room_by_id, update_room, delete_room
from app.controllers.booking_controller import create_booking, get_all_bookings, get_booking_by_id, update_booking_status, cancel_booking

main_bp = Blueprint("main", __name__)

main_bp.route("/hostels", methods=["POST"])(create_hostel)
main_bp.route("/hostels", methods=["GET"])(get_all_hostels)
main_bp.route("/hostels/<int:hostel_id>", methods=["GET"])(get_hostel_by_id)
main_bp.route("/hostels/<int:hostel_id>", methods=["PUT"])(update_hostel)
main_bp.route("/hostels/<int:hostel_id>", methods=["DELETE"])(delete_hostel)

main_bp.route("/rooms", methods=["POST"])(create_room)
main_bp.route("/rooms", methods=["GET"])(get_all_rooms)
main_bp.route("/rooms/<int:room_id>", methods=["GET"])(get_room_by_id)
main_bp.route("/rooms/<int:room_id>", methods=["PUT"])(update_room)
main_bp.route("/rooms/<int:room_id>", methods=["DELETE"])(delete_room)

main_bp.route("/bookings", methods=["POST"])(create_booking)
main_bp.route("/bookings", methods=["GET"])(get_all_bookings)
main_bp.route("/bookings/<int:booking_id>", methods=["GET"])(get_booking_by_id)
main_bp.route("/bookings/<int:booking_id>/status", methods=["PUT"])(update_booking_status)
main_bp.route("/bookings/<int:booking_id>/cancel", methods=["PUT"])(cancel_booking)