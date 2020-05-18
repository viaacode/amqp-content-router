#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/services/rabbit.py
#

import pika
import os
import requests
import json
import logging
import time


class RabbitClient:
    def __init__(self):
        # TODO: get from config
        self.RABBIT_EXCHANGE = ""
        self.RABBIT_QUEUE = ""
        self.RABBIT_USER = ""
        self.RABBIT_PASS = ""
        self.RABBIT_HOST = ""
        self.RABBIT_PORT = ""
        self.RABBIT_INCOMING_QUEUE = ""

        # TODO: Check if opening connection and channel is okay in __init__
        self.credentials = pika.PlainCredentials(self.RABBIT_USER, self.RABBIT_PASS)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.RABBIT_HOST, port=self.RABBIT_PORT, credentials=credentials,
            )
        )

        self.channel = connection.channel()

    def send_message(self, body, routing_key):
        try:
            self.channel.basic_publish(
                exchange=self.RABBIT_EXCHANGE, routing_key=routing_key, body=body
            )

            return True

        except pika.exceptions.AMQPConnectionError as ce:
            raise ce

    def on_message(self, channel, method_frame, header_frame, body):
        try:

            self.logger.info("RMQ_BRIDGE: on_message", body=body)

            message = {
                "delivery_tag": method_frame.delivery_tag,
                "message": body.decode("utf-8"),
            }

            res = requests.post(self.EVENT_LISTEN_URL, json=message, timeout=30.0)

            if res.status_code == 200:
                # Flask app received message with status 200-ok
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            else:
                # Later on we might choose to not ack here so that any failing messages are
                # kept on queue for a retry
                # but it might also block new messages from being processed (to be tested after deployed...)
                self.logger.warning(
                    "RMQBridge got error from service, discarding message",
                    response_content=res.content,
                )
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        except requests.exceptions.ReadTimeout as te:
            self.logger.error("RMQBridge: timeout error during processing", body=body)

    def listen(self, on_message_callback, queue = self.RABBIT_INCOMING_QUEUE):
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
