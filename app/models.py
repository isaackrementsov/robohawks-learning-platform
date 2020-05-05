from app import db
from sqlalchemy.orm import relationship


class Base(db.Mode):


    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_modified = db.Column(db.DateTime, default=db.func.current_timestamp())


    def save(self):
        db.session.add(self)
        db.session.commit()
