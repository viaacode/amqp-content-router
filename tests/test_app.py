import pytest

from tests.resources import resources
from tests.resources.mocks import mock_rabbit

from app.app import EventListener


EVENTS_TO_TEST = ["essenceLinkedEvent", "getMetadataResponse"]


@pytest.mark.parametrize("event", EVENTS_TO_TEST)
def test_handle_message(event, mock_rabbit, mocker):
    # ARRANGE
    xml = resources.load_xml_resource(event)

    eventListener = EventListener()
    spy = mocker.spy(eventListener.rabbitClient, "send_message")

    routing_key = f"event.to.viaa.{event}"

    # ACT
    eventListener.handle_message(None, None, None, xml)

    # ASSERT
    spy.assert_called_with(body=xml, routing_key=routing_key)
    assert True
