import pytest
from app import create_app, db

@pytest.fixture(scope='function')
def client():
    flask_app = create_app('testing')
    test_client = flask_app.test_client()
    app_context = flask_app.app_context()
    app_context.push()
    db.engine.execute("CREATE EXTENSION IF NOT EXISTS ltree;")
    db.create_all()

    yield test_client

    db.session.remove()
    db.drop_all()
    app_context.pop()

@pytest.fixture
def make_headers():
    def _make_headers(user):
        token = user.generate_auth_token().decode('utf-8')
        headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            'Authorization': f'Bearer {token}'
        }
        return headers

    return _make_headers
