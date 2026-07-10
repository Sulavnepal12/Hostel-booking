from app.extension import db

class Hostel(db.Model):
    __tablename__ = "hostels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    price_per_bed = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.String(300))
    total_rooms = db.Column(db.Integer, default=0)
    warden_name = db.Column(db.String(100))
    warden_phone = db.Column(db.String(20))
    warden_email = db.Column(db.String(100))
    rooms = db.relationship("Room", backref="hostel", lazy=True)

    def __repr__(self):
        return f"<Hostel {self.name}>"