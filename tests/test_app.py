import pytest

from tests.resources import resources
from tests.resources.mocks import mock_rabbit

from app.app import EventListener


EVENTS_TO_TEST = ["essenceLinkedEvent", "getMetadataResponse"]


@pytest.mark.parametrize("event", EVENTS_TO_TEST)
def test_handle_message(event, mock_rabbit, mocker):
    # ARRANGE
    eventListener = EventListener()
    routing_key = f"event.to.viaa.{event}"

    xml = resources.load_xml_resource(event)
    spy = mocker.spy(eventListener.rabbitClient, "send_message")
    channel_mock = mocker.MagicMock()
    channel_mock.basic_ack = lambda arg: None
    method_mock = mocker.MagicMock()
    method_mock.delivery_tag = 1

    # ACT
    eventListener.handle_message(channel_mock, method_mock, None, xml)

    # ASSERT
    spy.assert_called_with(body=xml, routing_key=routing_key)
    assert True
