from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.config import config_by_name
import logging

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    CORS(app)
    api = Api(app)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Register resources
    from app.api.resources.document import DocumentProcess, HealthCheck
    api.add_resource(DocumentProcess, '/api/process-document')
    api.add_resource(HealthCheck, '/api/health')
    
    return app