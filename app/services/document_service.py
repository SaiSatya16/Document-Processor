# app/services/document_service.py
import pytesseract
from PIL import Image
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentService:
    # Common words to exclude from names
    COMMON_WORDS = {
        'INDIAN', 'INDIA', 'REPUBLIC', 'OF', 'MALE', 'FEMALE', 'DATE', 'BIRTH', 'PLACE',
        'NATIONALITY', 'SEX', 'HYDERABAD', 'DELHI', 'MUMBAI', 'CHENNAI', 'KOLKATA',
        'BANGALORE', 'TELANGANA', 'MAHARASHTRA', 'TAMIL', 'NADU', 'KERALA', 'GIVEN',
        'NAME', 'SURNAME', 'TYPE', 'SIGNATURE'
    }

    @staticmethod
    def extract_document_info(image):
        """
        Extract document information from any passport format
        Returns name, document number, and expiration date
        """
        try:
            # Convert image to text using pytesseract
            text = pytesseract.image_to_string(image)
            logger.debug("Extracted text from image")
            
            # Initialize results
            result = {
                'name': None,
                'document_number': None,
                'expiration_date': None
            }
            
            # Split text into lines and clean them
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Log lines for debugging
            for i, line in enumerate(lines):
                logger.debug(f"Line {i}: {line}")
            
            # Common patterns
            patterns = {
                'passport_number': [
                    r'(?<![\w\d])([A-Z]\d{7})(?![\w\d])',
                    r'Passport No.*?([A-Z]\d{7})',
                    r'Number.*?([A-Z]\d{7})'
                ],
                'name_headers': [
                    r'Surname',
                    r'Given Name\(s\)',
                    r'Name'
                ],
                'expiry_headers': [
                    r'Date of Expiry|Expiry|Expiration|Valid Until|Valid Till',
                    r'समाप्ति की तिथि|समाप्ति',
                    r'Validity|Expires|Exp|Expiry Date'
                ]
            }

            # Extract document number (same as before)
            for line in lines:
                if '<' in line and any(c.isdigit() for c in line):
                    mrz_match = re.search(r'(?<![\w\d])([A-Z]\d{7})(?![\w\d])', line)
                    if mrz_match:
                        result['document_number'] = mrz_match.group(1)
                        break
            
            if not result['document_number']:
                for line in lines:
                    for pattern in patterns['passport_number']:
                        if match := re.search(pattern, line, re.IGNORECASE):
                            result['document_number'] = match.group(1) if '(' in pattern else match.group()
                            result['document_number'] = result['document_number'].strip()
                            break
                    if result['document_number']:
                        break

            # Improved name extraction
            name_parts = []
            
            # Method 1: Look for exact name field matches
            for i, line in enumerate(lines):
                # Look specifically for surname
                if 'Surname' in line or 'उपनाम' in line:
                    if i + 1 < len(lines):
                        surname = lines[i + 1].strip()
                        if surname and all(c.isalpha() or c.isspace() for c in surname):
                            if surname.upper() not in DocumentService.COMMON_WORDS:
                                name_parts.append(surname)
                
                # Look for given name
                if 'Given Name' in line or 'दिया गया नाम' in line:
                    if i + 1 < len(lines):
                        given_name = lines[i + 1].strip()
                        if given_name and all(c.isalpha() or c.isspace() for c in given_name):
                            if given_name.upper() not in DocumentService.COMMON_WORDS:
                                name_parts.insert(0, given_name)  # Insert at beginning

            # Method 2: Extract from MRZ line
            if not name_parts:
                for line in lines:
                    if '<' in line and result['document_number'] in line:
                        # Split MRZ line and look for name parts
                        parts = line.split('<')
                        for part in parts:
                            if part and part.isalpha() and len(part) > 1:
                                if part.upper() not in DocumentService.COMMON_WORDS:
                                    name_parts.append(part)

            # Method 3: Look for single-word names after specific headers
            if not name_parts:
                for i, line in enumerate(lines):
                    if any(header in line for header in ['Name', 'नाम']):
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if (next_line and 
                                all(c.isalpha() or c.isspace() for c in next_line) and 
                                next_line.upper() not in DocumentService.COMMON_WORDS):
                                name_parts.append(next_line)

            # Combine and clean up name
            if name_parts:
                # Remove duplicates while preserving order
                seen = set()
                name_parts = [x for x in name_parts if not (x in seen or seen.add(x))]
                
                # Join and clean
                result['name'] = ' '.join(name_parts)
                result['name'] = ' '.join(word for word in result['name'].split() 
                                        if word.upper() not in DocumentService.COMMON_WORDS)
                result['name'] = result['name'].upper()
                
                # Final validation - ensure it's not empty after cleaning
                if not result['name'].strip():
                    result['name'] = None

            # Date extraction (same as before)
            date_pattern = r'\b\d{2}[/-]\d{2}[/-]\d{0,4}\b'
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                if any(re.search(pattern, line_lower, re.IGNORECASE) for pattern in patterns['expiry_headers']):
                    dates = re.findall(date_pattern, line)
                    if dates:
                        result['expiration_date'] = dates[-1]
                        break
                    
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        dates = re.findall(date_pattern, next_line)
                        if dates:
                            result['expiration_date'] = dates[-1]
                            break

            if not result['expiration_date']:
                for line in lines:
                    dates = re.findall(date_pattern, line)
                    if len(dates) == 2:
                        result['expiration_date'] = dates[1]
                        break

            # Ensure date is in correct format
            if result['expiration_date']:
                if len(result['expiration_date']) == 8:
                    year = result['expiration_date'][-2:]
                    century = '20' if int(year) < 50 else '19'
                    result['expiration_date'] = result['expiration_date'][:-2] + century + year
            
            logger.info("Extracted information: %s", result)
            return result
            
        except Exception as e:
            logger.error(f"Error in extract_document_info: {str(e)}")
            raise