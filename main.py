from flask import Flask
from app.endpoints.feedback_endpoint import feedback
from app.endpoints.pages_endpoints import pages

app = Flask(__name__)
app.register_blueprint(feedback)
app.register_blueprint(pages)

app.run(debug=True)