import pytest
from flask import Flask

from app.endpoints.pages_endpoints import pages

@pytest.fixture()
def app():
    app = Flask(__name__)
    app.register_blueprint(pages)
    app.testing = True
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_home_status(client):
    response = client.get("/home")
    assert response.status_code == 200
    
def test_send_feedback_status(client):
    response = client.get("/send_feedback")
    assert response.status_code == 200
    
def test_display_statistics_status(client):
    response = client.get("/display_statistics")
    assert response.status_code == 200
    
def test_display_feedbacks_status(client):
    response = client.get("/display_feedbacks")
    assert response.status_code == 200