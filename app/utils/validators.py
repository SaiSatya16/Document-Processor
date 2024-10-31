from werkzeug.utils import secure_filename
import os
from datetime import datetime

class DocumentValidator:
    @staticmethod
    def allowed_file(filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def validate_date(date_str):
        try:
            return bool(datetime.strptime(date_str, '%d/%m/%Y'))
        except ValueError:
            return False