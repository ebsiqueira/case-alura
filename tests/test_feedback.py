import pytest
from flask import Flask

from app.endpoints.feedback_endpoint import feedback

@pytest.fixture()
def app():
    app = Flask(__name__)
    app.register_blueprint(feedback)
    app.testing = True
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_feedback_status(client):
    data = {'feedback': 'Gostei muito do app!'}
    
    response = client.post("/feedback", json=data)
    assert response.status_code == 200
    
def test_feedback_response(client):
    data = {'feedback': 'Gostei muito do app!'}
    
    response = client.post("/feedback", json=data)
    
    assert "id" in response.json
    assert "sentiment" in response.json
    assert "requested_features" in response.json
    assert "code" in response.json["requested_features"][0]
    assert "reason" in response.json["requested_features"][0]
    
def test_positive_feedback(client):
    data = {'feedback': 'Gostei muito do app!'}
    
    response = client.post("/feedback", json=data)
    
    assert response.json['sentiment'] == 'POSITIVO'
    
def test_negative_feedback(client):
    data = {'feedback': 'Não gostei do app.'}
    
    response = client.post("/feedback", json=data)
    
    assert response.json['sentiment'] == 'NEGATIVO'
    
def test_feedback_spam(client):
    data = {'feedback': 'Adoro Florianópolis'}
    
    response = client.post("/feedback", json=data)
    
    assert "message" in response.json
    assert "SPAM detectado" in response.json['message']