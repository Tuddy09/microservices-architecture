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
        pass


def configure_views(app):
    pass
