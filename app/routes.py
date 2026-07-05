from flask import Blueprint
from app.controllers.hostel_controller import create_hostel
from app.controllers.room_controller import create_room

main_bp = Blueprint("main", __name__)

main_bp.route("/hostels", methods=["POST"])(create_hostel)
main_bp.route("/rooms", methods=["POST"])(create_room)