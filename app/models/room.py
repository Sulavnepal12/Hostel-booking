from app.extension import db

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    hostel_id = db.Column(db.Integer, db.ForeignKey("hostels.id"), nullable=False)

    def __repr__(self):
        return f"<Room {self.room_number}>"