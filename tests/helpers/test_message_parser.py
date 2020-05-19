from app.helpers import message_parser
from tests.resources import resources
import pytest

EVENTS_TO_TEST = ["essenceLinkedEvent", "getMetadataResponse"]


@pytest.mark.parametrize("event", EVENTS_TO_TEST)
def test_get_message_root_tag(event):
    # ARRANGE
    xml = resources.load_xml_resource(event)

    # ACT
    root_tag = message_parser.get_message_root_tag(xml)

    # ASSERT
    assert root_tag == event
