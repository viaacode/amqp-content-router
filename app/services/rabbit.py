#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/services/rabbit.py
#

import json
import logging
import os
import time

from viaa.configuration import ConfigParser
from viaa.observability import logging

import pika


class RabbitClient:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.rabbitConfig = configParser.app_cfg["rabbitmq"]

        # TODO: Check if opening connection and channel is okay in __init__
        self.credentials = pika.PlainCredentials(
            self.rabbitConfig["user"], self.rabbitConfig["passwd"]
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitConfig["host"],
                port=self.rabbitConfig["port"],
                credentials=self.credentials,
            )
        )

        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.rabbitConfig["exchange"],
            exchange_type=self.rabbitConfig["exchange_type"],
            durable=True,
        )

        self.channel.queue_declare(queue=self.rabbitConfig["queue"], durable=True)

        self.channel.queue_bind(
            exchange=self.rabbitConfig["exchange"],
            queue=self.rabbitConfig["queue"],
            routing_key=self.rabbitConfig["routing_key"],
        )

    def send_message(self, body, routing_key):
        try:
            self.channel.basic_publish(
                exchange=self.rabbitConfig["exchange"],
                routing_key=routing_key,
                body=body,
            )

            return True

        except pika.exceptions.AMQPConnectionError as ce:
            raise ce

    def listen(self, on_message_callback, queue=None):
        if queue is None:
            queue = self.rabbitConfig["queue"]

        try:
            while True:
                try:
                    channel = self.connection.channel()

                    channel.basic_consume(
                        queue=queue, on_message_callback=on_message_callback
                    )

                    channel.start_consuming()
                except pika.exceptions.StreamLostError:
                    self.logger.warning("RMQBridge lost connection, reconnecting...")
                    time.sleep(3)
                except pika.exceptions.ChannelWrongStateError:
                    self.logger.warning(
                        "RMQBridge wrong state in channel, reconnecting..."
                    )
                    time.sleep(3)
                except pika.exceptions.AMQPHeartbeatTimeout:
                    self.logger.warning(
                        "RMQBridge heartbeat timed out, reconnecting..."
                    )
                    time.sleep(3)

        except KeyboardInterrupt:
            channel.stop_consuming()

        connection.close()
