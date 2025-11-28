import unittest
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import requests
from requests import RequestException
from pydantic import AnyHttpUrl
from filip.clients.base_http_client import NgsiURLVersion, BaseHttpClient
from filip.models.base import FiwareHeader, DataType
from filip.utils.simple_ql import QueryString
from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient
from filip.clients.ngsi_v2 import HttpClient, HttpClientConfig
from filip.config import settings
from filip.models.ngsi_v2.context import (
    ContextEntity,
    ContextAttribute,
    NamedContextAttribute,
    NamedCommand,
    Query,
    ActionType,
    ContextEntityKeyValues,
)


class TestContextBroker(unittest.TestCase):
    """
    Test class for ContextBrokerClient
    """

    def setUp(self) -> None:
        """
        Setup test data
        Returns:
            None
        """
        self.fiware_header = FiwareHeader(
            service=settings.FIWARE_SERVICE, service_path=settings.FIWARE_SERVICEPATH
        )
        self.resources = {
            "entities_url": "/v2/entities",
            "types_url": "/v2/types",
            "subscriptions_url": "/v2/subscriptions",
            "registrations_url": "/v2/registrations",
        }
        self.attr = {"temperature": {"value": 20.0, "type": "Number"}}
        self.entity = ContextEntity(id="MyId", type="MyType", **self.attr)

        self.iotac = IoTAClient(
            url=settings.IOTA_JSON_URL, fiware_header=self.fiware_header
        )

        self.client = ContextBrokerClient(
            url=settings.CB_URL, fiware_header=self.fiware_header
        )
        self.subscription = Subscription.model_validate(
            {
                "description": "One subscription to rule them all",
                "subject": {
                    "entities": [{"idPattern": ".*", "type": "Room"}],
                    "condition": {
                        "attrs": ["temperature"],
                        "expression": {"q": "temperature>40"},
                    },
                },
                "notification": {
                    "http": {"url": "http://localhost:1234"},
                    "attrs": ["temperature", "humidity"],
                },
                "expires": datetime.now() + timedelta(days=1),
                "throttling": 0,
            }
        )
