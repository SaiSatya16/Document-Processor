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
        'NAME', 'SURNAME', 'TYPE', 'SIGNATURE', 'DRIVING', 'LICENCE', 'LICENSE', 'UNION',
        'ISSUED', 'BY', 'STATE'
    }

    @staticmethod
    def extract_document_info(image):
        """
        Extract document information from passport or driving license
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
            
            # Detect document type
            is_driving_license = any('driving' in line.lower() for line in lines)
            
            # Document number patterns
            patterns = {
                'passport_number': [
                    r'(?<![\w\d])([A-Z]\d{7})(?![\w\d])',
                    r'Passport No.*?([A-Z]\d{7})',
                    r'Number.*?([A-Z]\d{7})'
                ],
                'driving_license_number': [
                    r'([A-Z]{2}\d{14})',  # Format: TS10720230011058
                    r'([A-Z]{2}\d{2}\d{12})'  # Alternative format with year separated
                ],
                'name_headers': [
                    r'Name[:|\s]*(.*)',
                    r'Given Name\(s\)',
                    r'Surname'
                ],
                'expiry_headers': [
                    r'Date of Expiry|Expiry|Expiration|Valid Until|Valid Till|Validity',
                    r'समाप्ति की तिथि|समाप्ति',
                    r'Validity \((?:NT|TR)\)'  # Specific to driving license
                ]
            }

            # Extract document number based on document type
            if is_driving_license:
                for line in lines:
                    for pattern in patterns['driving_license_number']:
                        if match := re.search(pattern, line):
                            result['document_number'] = match.group(1)
                            break
                    if result['document_number']:
                        break
            else:
                # Existing passport number extraction logic
                for line in lines:
                    if '<' in line and any(c.isdigit() for c in line):
                        mrz_match = re.search(r'(?<![\w\d])([A-Z]\d{7})(?![\w\d])', line)
                        if mrz_match:
                            result['document_number'] = mrz_match.group(1)
                            break

                # Fallback passport number extraction
                if not result['document_number']:
                    for line in lines:
                        for pattern in patterns['passport_number']:
                            if match := re.search(pattern, line):
                                result['document_number'] = match.group(1)
                                break
                        if result['document_number']:
                            break

            # Name extraction
            for i, line in enumerate(lines):
                # For driving license - direct name field
                if 'Name:' in line or line.strip().startswith('Name'):
                    name_parts = line.split(':', 1)
                    if len(name_parts) > 1:
                        result['name'] = name_parts[1].strip()
                    elif i + 1 < len(lines):
                        result['name'] = lines[i + 1].strip()
                    break
                
                # Look for name after "Name" text
                if line.strip() == 'Name' and i + 1 < len(lines):
                    result['name'] = lines[i + 1].strip()
                    break

            # Existing passport name extraction as fallback
            if not result['name']:
                name_parts = []
                for i, line in enumerate(lines):
                    if 'Surname' in line or 'उपनाम' in line:
                        if i + 1 < len(lines):
                            surname = lines[i + 1].strip()
                            if surname and all(c.isalpha() or c.isspace() for c in surname):
                                name_parts.append(surname)
                    
                    if 'Given Name' in line or 'दिया गया नाम' in line:
                        if i + 1 < len(lines):
                            given_name = lines[i + 1].strip()
                            if given_name and all(c.isalpha() or c.isspace() for c in given_name):
                                name_parts.insert(0, given_name)

                if name_parts:
                    result['name'] = ' '.join(name_parts)

            # Clean up name
            if result['name']:
                # Remove common words and clean up
                result['name'] = ' '.join(word for word in result['name'].split() 
                                        if word.upper() not in DocumentService.COMMON_WORDS)
                result['name'] = result['name'].upper().strip()
                
                # Final validation
                if not result['name'].strip():
                    result['name'] = None

            # Enhanced date extraction
            date_patterns = [
                r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',  # DD/MM/YYYY or DD-MM-YYYY
                r'\b\d{2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}\b',  # DD MMM YYYY
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{2},?\s*\d{4}\b'  # MMM DD, YYYY
            ]

            expiry_keywords = [
                'expiry', 'expires', 'exp', 'valid until', 'valid till', 
                'validity', 'date of expiry', 'expiration'
            ]

            def parse_date(date_str):
                try:
                    # Try different date formats
                    formats = [
                        '%d/%m/%Y', '%d-%m-%Y',
                        '%d %b %Y', '%d %B %Y',
                        '%b %d, %Y', '%B %d, %Y',
                        '%b %d %Y', '%B %d %Y'
                    ]
                    
                    for fmt in formats:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                    return None
                except Exception:
                    return None

            def extract_dates_from_line(line):
                dates = []
                for pattern in date_patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        date_str = match.group()
                        parsed_date = parse_date(date_str)
                        if parsed_date:
                            dates.append((parsed_date, date_str))
                return dates

            # First try to find dates near expiry keywords
            all_dates = []
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Check if line contains expiry keywords
                if any(keyword in line_lower for keyword in expiry_keywords):
                    # Check current line for dates
                    dates = extract_dates_from_line(line)
                    if dates:
                        all_dates.extend(dates)
                    
                    # Check next line for dates
                    if i + 1 < len(lines):
                        dates = extract_dates_from_line(lines[i + 1])
                        if dates:
                            all_dates.extend(dates)

            # If no dates found near expiry keywords, collect all dates
            if not all_dates:
                for line in lines:
                    dates = extract_dates_from_line(line)
                    all_dates.extend(dates)

            # Sort dates and select the latest one as expiration
            if all_dates:
                all_dates.sort(key=lambda x: x[0])  # Sort by datetime object
                result['expiration_date'] = all_dates[-1][1]  # Use the original string format

            logger.info("Extracted information: %s", result)
            return result
            
        except Exception as e:
            logger.error(f"Error in extract_document_info: {str(e)}")
            raise

