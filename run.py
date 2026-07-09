from app import create_app
from app.extension import db
from app.models.hostel import Hostel
from app.models.room import Room
from app.models.booking import Booking
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)