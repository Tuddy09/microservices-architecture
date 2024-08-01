import json

import redis
from decouple import Config
from flask import request


class Weather:
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
                d[k] = self.__dict__[k]
        return d


def configure_views(app):
    @app.route('/weather', methods=['GET'])
    def get_weather():
        city = request.args.get('city')
        date = request.args.get('date')
        if not city and not date:
            weather = []
            for key in client.keys():
                weather.append(json.loads(client.get(key)))
            return weather, 200
        else:
            for key in client.keys():
                weather = json.loads(client.get(key))
                if weather['city'] == city and weather['date'] == date:
                    return [weather], 200

    @app.route('/weather', methods=['POST'])
    def create_weather():
        data = request.get_json()
        id = data.get('id')
        city = data.get('city')
        date = data.get('date')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        description = data.get('description')
        weather = Weather(id, city, date, temperature, humidity, description)
        client.set(id, json.dumps(weather.to_dict()))
        return 'OK', 201

    @app.route('/weather', methods=['PUT'])
    def update_weather():
        data = request.get_json()
        id = request.args.get('id')
        city = data.get('city')
        date = data.get('date')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        description = data.get('description')
        weather = Weather(id, city, date, temperature, humidity, description)
        client.set(id, json.dumps(weather.to_dict()))
        return 'OK', 200

    @app.route('/weather', methods=['DELETE'])
    def delete_weather():
        id = request.args.get('id')
        client.delete(id)
        return 'OK', 200


client = redis.Redis(host='redis-db')

weathers = {
    "1": Weather(1, 'Brasov', '2021-07-01', 25, 50, 'Sunny'),
    "2": Weather(2, 'Bucuresti', '2021-07-01', 30, 60, 'Rainy')
}

for key, weather in weathers.items():
    client.set(key, json.dumps(weather.to_dict()))
