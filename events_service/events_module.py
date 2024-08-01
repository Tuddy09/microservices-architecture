from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from microskel.db_module import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    city = Column(String(128))
    date = Column(Date)
    title = Column(String(128))
    description = Column(String(128))

    def __init__(self, id, city, date, title, description):
        self.id = id
        self.city = city
        self.date = date
        self.title = title
        self.description = description

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                d[k] = self.__dict__[k] if k != 'date' else self.__dict__[k].strftime('%Y-%m-%d')
        return d


def configure_views(app):
    @app.route('/events', methods=['GET'])
    def get_events(db: SQLAlchemy):
        try:
            city = request.args.get('city')
            if city:
                data = db.session.query(Event).filter_by(city=city).all()
                return [d.to_dict() for d in data]
            else:
                data = db.session.query(Event).all()
                return [d.to_dict() for d in data]
        except Exception as e:
            return str(e), 500

    @app.route('/events', methods=['POST'])
    def create_event(db: SQLAlchemy):
        try:
            data = request.get_json()
            id = data.get('id')
            city = data.get('city')
            date = data.get('date')
            title = data.get('title')
            description = data.get('description')
            e = Event(id=id, city=city, date=date, title=title, description=description)
            db.session.add(e)
            db.session.commit()
            return 'OK', 201
        except Exception as e:
            return str(e), 500

    @app.route('/events', methods=['PUT'])
    def update_event(db: SQLAlchemy):
        try:
            event_id = request.args.get('id')
            e = db.session.query(Event).filter_by(id=event_id).first()
            data = request.get_json()
            e.city = data.get('city')
            e.date = data.get('date')
            e.title = data.get('title')
            e.description = data.get('description')
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500

    @app.route('/events', methods=['DELETE'])
    def delete_event(db: SQLAlchemy):
        try:
            event_id = request.args.get('id')
            e = db.session.query(Event).filter_by(id=event_id).first()
            db.session.delete(e)
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500
