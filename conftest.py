import app
import pytest
import app as webapp


@pytest.fixture
def app():
    app = webapp.app
    return app
