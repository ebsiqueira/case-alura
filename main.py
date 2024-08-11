from flask import Flask
from app.endpoints.feedback_endpoint import feedback
from app.endpoints.pages_endpoints import pages

alumind = Flask(__name__)
alumind._static_folder = 'app/static'
alumind.register_blueprint(feedback)
alumind.register_blueprint(pages)

alumind.run(debug=True)