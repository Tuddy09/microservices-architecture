import requests
from flask import request
from injector import Module, Binder, singleton

from microskel.retry_mechanism_module import RetryMechanismStrategy
from microskel.service_discovery import ServiceDiscovery  # interfata


class GatewayProxy:
    def __init__(self, service):
        self.service = service

    def proxy_request(self, method, endpoint, url_parameters, body):
        service_name = endpoint
        retry_mechanism = self.service.injector.get(RetryMechanismStrategy)
        endpoint = self.service.injector.get(ServiceDiscovery).discover(endpoint)
        url = f"{endpoint.to_base_url()}/weather" if service_name == 'weather-service' else f"{endpoint.to_base_url()}/events"
        try:
            if not endpoint:
                return 'No endpoint', 401
            if method == 'GET':
                if not url_parameters:
                    return requests.get(url)
                return requests.get(f'{url}?{url_parameters}')
            elif method == 'POST':
                return requests.post(f'{url}', json=body)
            elif method == 'PUT':
                return requests.put(f'{url}?{url_parameters}', json=body)
            elif method == 'DELETE':
                return requests.delete(f'{url}?{url_parameters}')
        except requests.exceptions.RequestException as e:
            return retry_mechanism.retry_algorithm(method, url, url_parameters, body)


class GatewayServiceModule(Module):
    def __init__(self, gateway_service):
        self.gateway_service = gateway_service

    def configure(self, binder: Binder) -> None:
        gateway_proxy = GatewayProxy(self.gateway_service)
        binder.bind(GatewayProxy, to=gateway_proxy, scope=singleton)


def configure_views(app):
    @app.route('/weather', methods=['GET'])
    def get_weather(gateway_proxy: GatewayProxy):
        city = request.args.get('city')
        date = request.args.get('date')
        if city and date:
            params = f'city={city}&date={date}'
        else:
            params = None
        data = gateway_proxy.proxy_request('GET', 'weather-service', params, None)
        return data.json(), 200

    @app.route('/weather', methods=['POST'])
    def post_weather(gateway_proxy: GatewayProxy):
        data = request.get_json()
        return_data = gateway_proxy.proxy_request('POST', 'weather-service', None, data)
        if return_data.status_code == 201:
            return 'OK', 201

    @app.route('/weather', methods=['PUT'])
    def put_weather(gateway_proxy: GatewayProxy):
        id = request.args.get('id')
        id = f"id={id}"
        data = request.get_json()
        return_data = gateway_proxy.proxy_request('PUT', 'weather-service', id, data)
        if return_data.status_code == 200:
            return 'OK', 200

    @app.route('/weather', methods=['DELETE'])
    def delete_weather(gateway_proxy: GatewayProxy):
        id = request.args.get('id')
        id = f"id={id}"
        return_data = gateway_proxy.proxy_request('DELETE', 'weather-service', id, None)
        if return_data.status_code == 200:
            return 'OK', 200

    @app.route('/events', methods=['GET'])
    def get_event(gateway_proxy: GatewayProxy):
        city = request.args.get('city')
        if city:
            city = f'city={city}'
        else:
            city = None
        data = gateway_proxy.proxy_request('GET', 'events-service', city, None)
        return data.json(), 200

    @app.route('/events', methods=['POST'])
    def post_event(gateway_proxy: GatewayProxy):
        data = request.get_json()
        return_data = gateway_proxy.proxy_request('POST', 'events-service', None, data)
        if return_data.status_code == 201:
            return 'OK', 201

    @app.route('/events', methods=['PUT'])
    def put_event(gateway_proxy: GatewayProxy):
        id = request.args.get('id')
        id = f"id={id}"
        data = request.get_json()
        return_data = gateway_proxy.proxy_request('PUT', 'events-service', id, data)
        if return_data.status_code == 200:
            return 'OK', 200

    @app.route('/events', methods=['DELETE'])
    def delete_event(gateway_proxy: GatewayProxy):
        id = request.args.get('id')
        id = f"id={id}"
        return_data = gateway_proxy.proxy_request('DELETE', 'events-service', id, None)
        if return_data.status_code == 200:
            return 'OK', 200
