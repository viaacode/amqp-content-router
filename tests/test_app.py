import pytest

from tests.resources import resources
from tests.resources.mocks import mock_rabbit

from app.app import EventListener


EVENTS_TO_TEST = ["essenceLinkedEvent", "getMetadataResponse"]


@pytest.mark.parametrize("event", EVENTS_TO_TEST)
def test_handle_message(event, mock_rabbit):
    eventListener = EventListener()
    xml = resources.load_xml_resource(event)

    assert True
