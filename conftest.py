import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("RABBIT_MQ_USER", "user")
    monkeypatch.setenv("RABBIT_MQ_PASSWD", "passwd")
    monkeypatch.setenv("RABBIT_MQ_HOST", "host")
    monkeypatch.setenv("RABBITMQ_QUEUE", "queue")
    monkeypatch.setenv("RABBITMQ_EXCHANGE", "exchange")
