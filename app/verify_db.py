from app import create_app
from app.extension import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    print("Tables:", inspector.get_table_names())