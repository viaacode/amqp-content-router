import pytest


@pytest.fixture
def mock_rabbit(monkeypatch):
    def mock_init(self):
        print(f"Initiating Rabbit connection.")
        pass

    from app.services.rabbit import RabbitClient

    monkeypatch.setattr(RabbitClient, "__init__", mock_init)
