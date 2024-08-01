import gateway_proxy
from microskel.service_template import ServiceTemplate


class GatewayService(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [gateway_proxy.GatewayServiceModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [gateway_proxy]


if __name__ == '__main__':
    GatewayService().start()
