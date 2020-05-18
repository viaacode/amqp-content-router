#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/app.py
#

from viaa.configuration import ConfigParser
from viaa.observability import logging

from helper import message_parser
from services import rabbit

configParser = ConfigParser()
log = logging.get_logger(__name__, config=self.configParser)

# Declare rabbit client global so we can use it to listen and publish.
rabbitClient = rabbit.RabbitClient()


def handle_message(self, channel, method, header, body):
    # 1. Parse message
    root_tag = message_parser.get_message_root_tag(body)

    # 2. Construct correct routing_key
    routing_key = f"{configParser.app_cfg["routing_key_prefix"]}{root_tag}"

    # 3. Publish message with new routing key
    rabbitClient.send_message(body, routing_key)


def start():
    # Start listening for incoming messages
    rabbitClient.listen(handle_message)
