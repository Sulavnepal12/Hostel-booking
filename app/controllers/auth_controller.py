from flask import jsonify, request, session
from app.extension import db
from app.models.user import User


def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=data.get("username")).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 400

    new_user = User(username=data.get("username"))
    new_user.set_password(data.get("password"))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "id": new_user.id}), 201


def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id
    session["username"] = user.username

    return jsonify({"message": "Logged in successfully", "username": user.username}), 200


def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


def check_session():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session.get("username")}), 200
    return jsonify({"logged_in": False}), 200


def get_all_users():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    users = User.query.all()
    result = [{"id": u.id, "username": u.username} for u in users]
    return jsonify(result), 200


def delete_user(user_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    if session.get("user_id") == user_id:
        return jsonify({"error": "You cannot delete your own account while logged in."}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200