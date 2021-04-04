from app import db
from sqlalchemy.orm import relationship

class Base(db.Model):


    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_modified = db.Column(db.DateTime, default=db.func.current_timestamp())

    @staticmethod
    def lookup_id(entity_class, id):
        return entity_class.query.get(id)


    def save(self):
        db.session.add(self)
        self.update()

    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        self.update()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
