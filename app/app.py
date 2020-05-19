#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/app.py
#

from viaa.configuration import ConfigParser
from viaa.observability import logging

from app.helpers import message_parser
from app.services import rabbit


class EventListener:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.config = configParser.app_cfg
        self.rabbitClient = rabbit.RabbitClient()

    def handle_message(self, channel, method, properties, body):
        # 1. Parse message
        root_tag = message_parser.get_message_root_tag(body)

        # 2. Construct correct routing_key
        routing_key = f"{self.config['rabbitmq']['routing_key']}.{root_tag}"
        self.log.info(f"Publishing message with new routing key: {routing_key}.")

        # 3. Publish message with new routing key
        self.rabbitClient.send_message(body, routing_key)

        # 4. ack message
        channel.basic_ack(method.delivery_tag)

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
        self.rabbitClient.listen(self.handle_message)
