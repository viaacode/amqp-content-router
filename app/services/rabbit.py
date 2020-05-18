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
import requests

configParser = ConfigParser()
log = logging.get_logger(__name__, config=self.configParser)


class RabbitClient:
    def __init__(self):
        self.rabbitConfig = configParser.app_cfg["rabbitmq"]

        # TODO: Check if opening connection and channel is okay in __init__
        self.credentials = pika.PlainCredentials(
            self.rabbitConfig["user"], self.rabbitConfig["passwd"]
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitConfig["host"],
                port=self.rabbitConfig["port"],
                credentials=credentials,
            )
        )

        self.channel = connection.channel()

    def send_message(self, body, routing_key):
        outgoing_config = self.rabbitConfig["outgoing"]
        try:
            self.channel.basic_publish(
                exchange=outgoing_config["exchange"], routing_key=routing_key, body=body
            )

            return True

        except pika.exceptions.AMQPConnectionError as ce:
            raise ce

    def listen(self, on_message_callback, queue=None):
        incoming_config = self.rabbitConfig["incoming"]

        if queue is None:
            queue = incoming_config["queue"]

        try:
            while True:
                try:
                    channel = self.connection.channel()

                    # TODO: Check if application should declare queues
                    # result = channel.queue_declare(
                    #     queue=self.RABBIT_LISTEN_QUEUE, exclusive=False, durable=True
                    # )
                    # callback_queue = result.method.queue

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
