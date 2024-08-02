import random
import time
from abc import abstractmethod, ABC

import requests
from decouple import config
from injector import Module, Binder, singleton


class LoadBalancerStrategy(ABC):
    @abstractmethod
    def balance_load(self, registrations):
        pass


class RoundRobin_LB(LoadBalancerStrategy):
    def __init__(self):
        self.index = 0

    def balance_load(self, registrations):
        if not registrations:
            return None
        selected = registrations[self.index % len(registrations)]
        self.index += 1
        return selected


class LeastResponseTime_LB(LoadBalancerStrategy):
    def balance_load(self, registrations):
        if not registrations:
            return None

        def get_response_time(registration):
            try:
                start_time = time.time()
                response = requests.get(f'{registration.to_base_url()}/health')
                response.raise_for_status()
                return time.time() - start_time
            except requests.RequestException:
                return float('inf')

        return min(registrations, key=get_response_time)


def configure_views(app):
    pass
