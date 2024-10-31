# Document Processor

Document Processor is a full-stack web application that extracts and processes information from identity documents like passports and driving licenses. The application uses OCR (Optical Character Recognition) to automatically extract key information such as names, document numbers, and expiration dates.

## 🚀 Features

- **Document Upload**: Support for PNG, JPG, and JPEG formats (up to 16MB)
- **Information Extraction**: Automatically extracts:
  - Full Name
  - Document Number
  - Expiration Date
- **Modern UI**: Responsive design with drag-and-drop file upload
- **Real-time Preview**: View uploaded documents before processing
- **Error Handling**: Comprehensive error messages and validation
- **Toast Notifications**: User-friendly status updates

## 🛠️ Tech Stack

### Backend (Python/Flask)
- Flask: Web framework
- Flask-RESTful: REST API implementation
- Flask-CORS: Cross-origin resource sharing
- Pillow (PIL): Image processing
- Pytesseract: OCR engine
- Werkzeug: File handling and utilities

### Frontend (React)
- React 18
- React Router for navigation
- Tailwind CSS for styling
- Shadcn/ui for UI components
- Lucide React for icons
- Vite for build tooling

## 🐳 Docker Setup (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Quick Start
1. Clone the repository
```bash
git clone <repository-url>
cd document-processor
```

2. Create `.env` file in the root directory
```bash
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here
```

3. Build and run the containers
```bash
# Build and start all services
docker-compose up --build

# To run in detached mode
docker-compose up -d

# To stop all services
docker-compose down

# To view logs
docker-compose logs -f
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Docker Configuration Files

The project includes several Docker-related files:

- `Dockerfile` - Backend container configuration
- `document-processor_frontend/Dockerfile` - Frontend container configuration
- `docker-compose.yml` - Multi-container application setup
- `.dockerignore` - Files excluded from Docker context

### Docker Volumes

The application uses Docker volumes for:
- Persistent storage of uploaded files
- Hot-reloading of code changes during development

### Environment Variables

Docker Compose manages environment variables for:
- Flask configuration
- API endpoints
- Development/production modes

## 🚦 Manual Setup (Alternative)

### Prerequisites

1. Python 3.8+
2. Node.js 16+
3. Tesseract OCR engine
4. npm or yarn

### Backend Setup

1. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`

### Frontend Setup

1. Navigate to frontend directory
```bash
cd document-processor_frontend
```

2. Install dependencies
```bash
npm install
```

### Running Without Docker

#### Start Backend Server
```bash
python run.py
```
The server will start at `http://localhost:5000`

#### Start Frontend Development Server
```bash
cd document-processor_frontend
npm run dev
```
The application will be available at `http://localhost:5173`

## 📁 Project Structure

```bash
document-processor/
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── api/
│   │   └── resources/
│   │       └── document.py
│   ├── services/
│   │   └── document_service.py
│   ├── utils/
│   │   └── validators.py
│   ├── config.py
│   └── __init__.py
├── document-processor_frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── run.py
```

## 🔒 Configuration

### Backend Configuration
- Edit `app/config.py` to modify:
  - Allowed file extensions
  - Maximum file size
  - Environment-specific settings

### Frontend Configuration
- Edit `src/services/config.js` to modify:
  - API endpoint
  - File size limits
  - Allowed file types

### Docker Configuration
- Edit `docker-compose.yml` to modify:
  - Port mappings
  - Environment variables
  - Volume configurations

## 🧪 Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size limits
- OCR processing errors
- Network errors
- Server errors

## 🔐 Security Considerations

- File validation on both frontend and backend
- CORS configuration
- File size limits
- Allowed file type restrictions
- Input sanitization
- Docker container isolation
- Environment variable management


## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Flask](https://flask.palletsprojects.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Docker](https://www.docker.com/)