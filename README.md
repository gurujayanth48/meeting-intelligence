# AI Meeting Intelligence Platform

A web application that extracts actionable insights from meeting recordings using AI technologies. Upload your audio/video meetings and get automatically extracted action items, decisions, participants, and searchable content.

## 🚀 Features

- **File Upload**: Support for audio and video meeting recordings
- **Automatic Transcription**: Speech-to-text conversion using Whisper
- **AI Insights Extraction**: Action items, key decisions, participants, and topics
- **Semantic Search**: Search through meeting content with vector embeddings
- **Analytics Dashboard**: Visualize meeting data and trends
- **Responsive UI**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **Python FastAPI** - High-performance web framework
- **SQLite** - Lightweight database for data storage
- **Whisper.cpp** - Fast speech recognition engine
- **Ollama + Llama2** - Large language model for information extraction
- **ChromaDB** - Vector database for semantic search

### Frontend
- **React** - Modern JavaScript library for building user interfaces
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Declarative charting library

## 📋 Prerequisites

Before you begin, ensure you have installed:

- **Python 3.9 or higher**
- **Node.js 16 or higher**
- **npm or yarn**
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/gurujayanth48/meeting-intelligence-platform.git
cd meeting-intelligence-platform
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python app/main.py
```

### 3. Frontend Setup

Open a new terminal window and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. AI Services Setup

#### Whisper.cpp (Transcription)
```bash
# Clone Whisper.cpp
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# Build
make

# Download a model (tiny for testing, base for better accuracy)
bash ./models/download-ggml-model.sh tiny

# Run server (in separate terminal)
./server -m ./models/ggml-tiny.bin -t 4
```

#### Ollama (LLM)
```bash
# Install Ollama from https://ollama.ai

# Pull Llama2 model
ollama run llama2

# Keep Ollama running in background
```

#### ChromaDB (Vector Search)
```bash
# Install ChromaDB
pip install chromadb

# Run ChromaDB server
chroma run --path ./chroma-data
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=sqlite:///./meeting_insights.db

# AI Services
OLLAMA_API_URL=http://localhost:11434
CHROMA_HOST=localhost
CHROMA_PORT=8000
WHISPER_MODEL=base

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=100  # in MB

# Server
HOST=0.0.0.0
PORT=8000
```

### Configuration Files

#### Backend Configuration (`backend/app/core/config.py`)
```python
class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./meeting_insights.db")
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "100")) * 1024 * 1024
```

#### Frontend Configuration (`frontend/src/services/api.js`)
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🎯 Usage

### Starting the Application

1. **Start AI Services** (in separate terminals):
   ```bash
   # Terminal 1: Whisper server
   cd whisper.cpp
   ./server -m ./models/ggml-tiny.bin -t 4
   
   # Terminal 2: Ollama (keep running)
   ollama run llama2
   
   # Terminal 3: ChromaDB
   chroma run --path ./chroma-data
   ```

2. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python app/main.py
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Using the Platform

1. Open your browser and go to `http://localhost:5173`
2. Click "Upload New Meeting" and select an audio or video file
3. Wait for processing (this may take a few minutes for longer files)
4. View extracted insights, action items, and analytics
5. Use the search feature to find specific content in meetings

## 📡 API Endpoints

### Authentication
No authentication required for development version.

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload meeting recording |
| `GET` | `/api/meetings/{meeting_id}/status` | Get processing status |
| `GET` | `/api/meetings/{meeting_id}` | Get meeting insights |
| `GET` | `/api/meetings` | List all meetings |
| `POST` | `/api/search` | Search meeting content |

### Example API Usage

**Upload a file:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meeting_recording.mp3"
```

**Get meeting status:**
```bash
curl -X GET "http://localhost:8000/api/meetings/{meeting_id}/status"
```

## 📁 Project Structure

```
meeting-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes and models
│   │   ├── core/         # Configuration and database
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │  
│   ├── ai/
│   │   ├── transcription/ # Whisper client
│   │   ├── extraction/    # LLM client
│   │   └── search/        # ChromaDB client
│   ├── requirements.txt   # Python dependencies
│   └── app/main.py       # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── App.jsx       # Main app component
│   │   └── main.jsx      # Entry point
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│   └── tailwind.config.js # Tailwind configuration
├── README.md             # This file
└── .env                  # Environment variables
```

## 🔧 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Make sure you're in the correct directory
cd backend
pip install -r requirements.txt
```

**2. Database connection issues**
```bash
# Check if database file exists
ls -la backend/meeting_insights.db

# If not, run the app once to create it
python app/main.py
```

**3. AI services not responding**
```bash
# Check if services are running
curl http://localhost:8000/health  # Whisper
curl http://localhost:11434/api/tags  # Ollama
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB
```

**4. File upload too large**
```bash
# Increase max file size in .env
MAX_FILE_SIZE=500  # 500MB
```

### Logs and Debugging

**Backend logs:**
```bash
# Check for errors in terminal where backend is running
# Look for stack traces and error messages
```

**Frontend logs:**
```bash
# Check browser developer console (F12)
# Look for network errors and JavaScript errors
```

## 📈 Performance Tips

1. **For better transcription accuracy**: Use larger Whisper models (base, small, medium)
2. **For faster processing**: Use smaller models and optimize audio quality
3. **For production**: Consider using GPU-accelerated versions of AI services
4. **For large files**: Implement chunked processing and progress tracking


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Ollama](https://ollama.ai) for local LLM deployment
- [ChromaDB](https://www.trychroma.com/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for backend framework
- [React](https://reactjs.org/) for frontend framework

