"""

    python -m pytest --disable-warnings

"""

import pytest

from app import APP as APP

@pytest.fixture
def app():
    yield APP

@pytest.fixture
def client(app):
    return app.test_client()
