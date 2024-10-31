from flask_restful import Resource, reqparse
from flask import current_app
from werkzeug.datastructures import FileStorage
import io
from PIL import Image
from app.services.document_service import DocumentService
from app.utils.validators import DocumentValidator
import logging

logger = logging.getLogger(__name__)

class DocumentProcess(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('document',
                                type=FileStorage,
                                location='files',
                                required=True,
                                help='Document image is required')
    
    def post(self):
        try:
            args = self.parser.parse_args()
            file = args['document']
            
            # Validate file
            if file.filename == '':
                return {'error': 'No selected file'}, 400
                
            if not DocumentValidator.allowed_file(
                file.filename, 
                current_app.config['ALLOWED_EXTENSIONS']
            ):
                return {'error': 'Invalid file type'}, 400
                
            # Process image
            image = Image.open(io.BytesIO(file.read()))
            
            # Extract information
            document_info = DocumentService.extract_document_info(image)
            
            # Validate extracted information
            if not any(document_info.values()):
                return {
                    'error': 'Could not extract any information from the document',
                    'extracted_data': document_info
                }, 422
                
            return {
                'message': 'Document processed successfully',
                'data': document_info
            }, 200
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return {'error': 'Internal server error'}, 500

class HealthCheck(Resource):
    def get(self):
        return {'status': 'healthy'}, 200