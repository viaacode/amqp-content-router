#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/app.py
#

import lxml.etree as etree
import pika.exceptions
from viaa.configuration import ConfigParser
from viaa.observability import logging

from app.helpers import message_parser
from app.services import rabbit


class EventListener:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.config = configParser.app_cfg
        try:
            self.rabbitClient = rabbit.RabbitClient()
        except pika.exceptions.AMQPConnectionError as error:
            self.log.error("Connection to RabbitMQ failed.")
            raise error

    def handle_message(self, channel, method, properties, body):
        try:
            root_tag = message_parser.get_message_root_tag(body)
        except etree.XMLSyntaxError as syntaxError:
            self.log.error("Message is not valid XML!", error=syntaxError)

            # Off to the dead-letter queue it goes.
            channel.basic_reject(method.delivery_tag, requeue=False)
            return

        routing_key = f"{method.routing_key}.{root_tag}"
        self.log.info(f"Publishing message with new routing key: {routing_key}.")

        try:
            self.rabbitClient.send_message(body, routing_key)

            channel.basic_ack(method.delivery_tag)
        except pika.exceptions.AMQPError as error:
            self.log.critical(
                "Failed to publish message!",
                error=error,
                body=body,
                routing_key=routing_key,
            )

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
        self.rabbitClient.listen(self.handle_message)
