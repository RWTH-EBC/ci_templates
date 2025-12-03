import unittest
from filip.models.base import FiwareHeader
from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient, QuantumLeapClient
from filip.config import settings


class TestHealthCheck(unittest.TestCase):
    def setUp(self) -> None:
        self.fiware_header = FiwareHeader(
            service=settings.FIWARE_SERVICE,
        )
        self.iotac = IoTAClient(
            url=settings.IOTA_URL, fiware_header=self.fiware_header
        )

        self.cbc = ContextBrokerClient(
            url=settings.CB_URL, fiware_header=self.fiware_header
        )
        self.qlc = QuantumLeapClient(
            url=settings.QL_URL, fiware_header=self.fiware_header
        )

    def test_fiware_health_check(self):
        cbv = self.cbc.get_version()
        print(cbv)
        iotv = self.iotac.get_version()
        print(iotv)
        qlv = self.qlc.get_version()
        print(qlv)

