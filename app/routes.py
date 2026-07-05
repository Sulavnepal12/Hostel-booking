from flask import Blueprint
from app.controllers.hostel_controller import create_hostel, get_all_hostels, get_hostel_by_id
from app.controllers.room_controller import create_room, get_all_rooms, get_room_by_id

main_bp = Blueprint("main", __name__)

main_bp.route("/hostels", methods=["POST"])(create_hostel)
main_bp.route("/hostels", methods=["GET"])(get_all_hostels)
main_bp.route("/hostels/<int:hostel_id>", methods=["GET"])(get_hostel_by_id)

main_bp.route("/rooms", methods=["POST"])(create_room)
main_bp.route("/rooms", methods=["GET"])(get_all_rooms)
main_bp.route("/rooms/<int:room_id>", methods=["GET"])(get_room_by_id)