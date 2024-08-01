import events_module
from microskel.service_template import ServiceTemplate


class EventsService(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    def get_python_modules(self):
        return super().get_python_modules() + [events_module]


if __name__ == '__main__':
    EventsService('events_service').start()
