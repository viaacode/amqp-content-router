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
    method_mock = mocker.MagicMock()
    method_mock.delivery_tag = 1

    # ACT
    eventListener.handle_message(channel_mock, method_mock, None, xml)

    # ASSERT
    spy.assert_called_with(xml, routing_key)


def test_handle_invalid_message(mock_rabbit, mocker, capsys):
    # ARRANGE
    eventListener = EventListener()

    xml = "<broken></roken>"
    spy = mocker.spy(eventListener.rabbitClient, "send_message")
    channel_mock = mocker.MagicMock()
    method_mock = mocker.MagicMock()
    method_mock.delivery_tag = 1

    # ACT
    eventListener.handle_message(channel_mock, method_mock, None, xml)
    captured = capsys.readouterr()

    # ASSERT
    assert not spy.called
    assert "error" in captured.out


def test_start(mock_rabbit, mocker):
    # ARRANGE
    eventListener = EventListener()
    spy = mocker.spy(eventListener.rabbitClient, "listen")

    # ACT
    eventListener.start()

    # ASSERT
    spy.assert_called_with(eventListener.handle_message)
