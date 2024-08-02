import random
import time
from abc import abstractmethod, ABC

import requests
from decouple import config
from injector import Module, Binder, singleton


class RetryMechanismStrategy(ABC):
    @abstractmethod
    def retry_algorithm(self, method, url, url_parameters, body):
        pass


class ExponentialBackoff(RetryMechanismStrategy):
    def retry_algorithm(self, method, url, url_parameters, body):
        retry_delay = 1
        max_retries = 5
        for attempt in range(max_retries):
            try:
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
            except requests.RequestException as e:
                retry_delay *= 2
                time.sleep(retry_delay)


class RetryWithJitter(RetryMechanismStrategy):
    def retry_algorithm(self, method, url, url_parameters, body):
        retry_delay = 1
        max_retries = 5
        for attempt in range(max_retries):
            try:
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
            except requests.RequestException as e:
                retry_delay *= 2
                time.sleep(retry_delay)
                retry_delay += random.uniform(0, 1)


class RetryMechanismModule(Module):
    def configure(self, binder: Binder) -> None:
        if config('RETRY_MECHANISM') == 'exponential_backoff':
            strategy = ExponentialBackoff()
        else:
            strategy = RetryWithJitter()
        binder.bind(RetryMechanismStrategy, to=strategy, scope=singleton)


def configure_views(app):
    pass
