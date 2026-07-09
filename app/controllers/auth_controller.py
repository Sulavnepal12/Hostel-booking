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