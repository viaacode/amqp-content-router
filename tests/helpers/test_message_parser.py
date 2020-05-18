from app.helpers import message_parser


def test_essence_linked():
    root_tag = message_parser.get_message_root_tag("<xml></xml>")

    assert root_tag == "essenceLinked"
