import os
from flask import jsonify, request, current_app
from werkzeug.utils import secure_filename
from app.extension import db
from app.models.room import Room

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file):
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(upload_folder, filename)
            counter += 1
        file.save(filepath)
        return f"/static/uploads/{filename}"
    return None


def delete_image_file(image_url):
    if image_url and image_url.startswith("/static/uploads/"):
        full_path = os.path.join(current_app.root_path, "static", "uploads", os.path.basename(image_url))
        if os.path.exists(full_path):
            os.remove(full_path)


def create_room():
    if request.content_type and "multipart/form-data" in request.content_type:
        data = request.form
        image_file = request.files.get("image")
    else:
        data = request.get_json() or {}
        image_file = None

    if not data.get("room_number") or not data.get("hostel_id"):
        return jsonify({"error": "Room number and hostel_id are required"}), 400

    image_url = save_uploaded_image(image_file) if image_file else data.get("image_url")

    new_room = Room(
        room_number=data.get("room_number"),
        room_type=data.get("room_type"),
        capacity=data.get("capacity"),
        is_available=True,
        image_url=image_url,
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
            "image_url": r.image_url,
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
        "image_url": room.image_url,
        "hostel_id": room.hostel_id
    }), 200


def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if request.content_type and "multipart/form-data" in request.content_type:
        data = request.form
        image_file = request.files.get("image")
    else:
        data = request.get_json() or {}
        image_file = None

    if image_file and image_file.filename:
        new_image_url = save_uploaded_image(image_file)
        if new_image_url:
            delete_image_file(room.image_url)
            room.image_url = new_image_url
    elif data.get("image_url"):
        room.image_url = data.get("image_url")

    room.room_number = data.get("room_number", room.room_number)
    room.room_type = data.get("room_type", room.room_type)
    room.capacity = data.get("capacity", room.capacity)
    if "hostel_id" in data:
        room.hostel_id = data.get("hostel_id")

    db.session.commit()

    return jsonify({"message": "Room updated successfully", "id": room.id}), 200


def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    delete_image_file(room.image_url)

    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Room deleted successfully"}), 200