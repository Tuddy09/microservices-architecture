from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from microskel.db_module import Base


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city = Column(String(128))
    date = Column(Date)
    temperature = Column(Float)
    humidity = Column(Integer)
    description = Column(String(128))

    def __init__(self, id, city, date, temperature, humidity, description):
        self.id = id
        self.city = city
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.description = description

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                d[k] = self.__dict__[k] if k != 'date' else self.__dict__[k].strftime('%Y-%m-%d')
        return d


def configure_views(app):
    @app.route('/weather', methods=['GET'])
    def get_weather(db: SQLAlchemy):
        try:
            city = request.args.get('city')
            date = request.args.get('date')
            if city and date:
                data = db.session.query(Weather).filter_by(city=city, date=date).all()
                return [d.to_dict() for d in data]
            else:
                data = db.session.query(Weather).all()
                return [d.to_dict() for d in data]
        except Exception as e:
            return str(e), 500

    @app.route('/weather', methods=['POST'])
    def create_weather(db: SQLAlchemy):
        try:
            data = request.get_json()
            id = data.get('id')
            city = data.get('city')
            date = data.get('date')
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            description = data.get('description')
            w = Weather(id=id, city=city, date=date, temperature=temperature, humidity=humidity,
                        description=description)
            db.session.add(w)
            db.session.commit()
            return 'OK', 201
        except Exception as e:
            return str(e), 500

    @app.route('/weather', methods=['PUT'])
    def update_weather(db: SQLAlchemy):
        try:
            event_id = request.args.get('id')
            e = db.session.query(Weather).filter_by(id=event_id).first()
            data = request.get_json()
            e.city = data.get('city')
            e.date = data.get('date')
            e.title = data.get('title')
            e.description = data.get('description')
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500

    @app.route('/weather', methods=['DELETE'])
    def delete_weather(db: SQLAlchemy):
        try:
            event_id = request.args.get('id')
            w = db.session.query(Weather).filter_by(id=event_id)
            db.session.delete(w)
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500
