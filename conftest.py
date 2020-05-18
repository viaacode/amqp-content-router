import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("RABBIT_MQ_USER", "user")
    monkeypatch.setenv("RABBIT_MQ_PASSWD", "passwd")
    monkeypatch.setenv("RABBIT_MQ_HOST", "host")
    monkeypatch.setenv("RABBITMQ_INCOMING_QUEUE", "incoming_queue")
    monkeypatch.setenv("RABBITMQ_INCOMING_EXCHANGE", "incoming_exchange")
    monkeypatch.setenv("RABBITMQ_OUTGOING_QUEUE", "outgoing_queue")
    monkeypatch.setenv("RABBITMQ_OUTGOING_EXCHANGE", "outgoing_exchange")
