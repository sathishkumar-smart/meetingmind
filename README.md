# 🎙️ MeetingMind - AI Meeting Transcription & Summarization

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An **AI-powered meeting transcription and summarization application** that transforms audio recordings into actionable insights. Built with production-ready architecture, featuring real speech-to-text transcription, intelligent LLM routing, batch processing, and multiple export formats.

## 🌟 Features

### Core Capabilities
- **🎤 Real Speech-to-Text** - OpenAI Whisper integration for accurate transcription
- **🤖 AI Summarization** - Intelligent LLM routing (Ollama → Groq fallback)
- **📊 Action Items Extraction** - Automatically identify tasks and owners
- **🏷️ Topic Detection** - AI-powered meeting topic classification
- **📝 Meeting Transcript** - Full text transcript with word count

### Advanced Features
- **📁 Batch Upload** - Process multiple audio files simultaneously
- **📄 Multi-Format Export** - Download as Markdown or PDF
- **🔍 Full-Text Search** - Search by title, description, or content
- **🌙 Dark Mode UI** - Beautiful, responsive dark/light theme
- **⚡ Real-Time Updates** - Live status polling during processing
- **📱 Responsive Design** - Works on desktop and mobile

### Architecture Highlights
- **Smart LLM Provider Routing** - Checks Ollama first (free, local), falls back to Groq (free tier)
- **Zero Vendor Lock-In** - Switch between LLM providers with zero code changes
- **Batch Processing** - Upload 1-10 files, all process in parallel
- **PostgreSQL Backend** - Production-grade database with full ORM support
- **RESTful API** - Clean, documented endpoints with Swagger UI

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern async web framework |
| **Python 3.12** | Core language |
| **SQLAlchemy** | ORM for database abstraction |
| **PostgreSQL** | Production database |
| **Whisper** | Speech-to-text transcription |
| **Groq API** | Cloud LLM fallback |
| **Ollama** | Local LLM (Mistral/Phi models) |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type-safe development |
| **Axios** | HTTP client |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |

### DevOps
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **PostgreSQL** | Relational database |
| **Git** | Version control |

## 📋 Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Ollama** (optional, for local AI)
- **4GB RAM minimum** (8GB recommended)
- **FFmpeg** (for audio processing)

## 🚀 Quick Start

### 1. Clone Repository

git clone https://github.com/sathishkumar-smart/meetingmind.git
cd meetingmind

### 2. Backend Setup

cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env

### 3. Configure Environment
Edit `backend/.env`:

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost/meetingmind

# LLM Provider (choose one)
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here

# Or use local Ollama
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434


### 4. Setup PostgreSQL

sudo -u postgres psql
CREATE DATABASE meetingmind;
ALTER USER postgres WITH PASSWORD 'postgres';


### 5. Start Backend

uvicorn app.main:app --reload --port 8000

Backend will be available at: **http://localhost:8000**

### 6. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: **http://localhost:5173**

## 📖 API Documentation

### Interactive Swagger UI

http://localhost:8000/docs

### Key Endpoints

#### Meetings
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/meetings` | Upload audio file |
| GET | `/api/v1/meetings` | List all meetings |
| GET | `/api/v1/meetings/{id}` | Get meeting details |
| DELETE | `/api/v1/meetings/{id}` | Delete meeting |
| GET | `/api/v1/meetings/search?query=...` | Search meetings |

#### Exports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/meetings/{id}/export/markdown` | Download as Markdown |
| GET | `/api/v1/meetings/{id}/export/pdf` | Download as PDF |

#### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health check |
| GET | `/llm-status` | Current LLM provider info |
| GET | `/docs` | Swagger API docs |

## 🎯 Use Cases

✅ **Team Meetings** - Automatically summarize standup meetings  
✅ **Client Calls** - Generate meeting notes and action items  
✅ **Training Sessions** - Create transcripts and key takeaways  
✅ **Interviews** - Transcribe and summarize interviews  
✅ **Lectures** - Generate lecture notes and summaries  

## 🏗️ Architecture

MeetingMind/
├── backend/                          # FastAPI application
│   ├── app/
│   │   ├── core/                     # Configuration
│   │   ├── models/                   # Database ORM models
│   │   ├── schemas/                  # Pydantic validation
│   │   ├── services/                 # Business logic
│   │   │   ├── llm_service.py       # ⭐ LLM routing (Ollama → Groq)
│   │   │   ├── audio_service.py     # Audio processing & Whisper
│   │   │   ├── meeting_service.py   # Meeting CRUD
│   │   │   └── export_service.py    # PDF/Markdown export
│   │   └── routers/                  # API endpoints
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                         # React application
├── src/
│   ├── App.tsx                  # Main component
│   └── components/              # React components
├── package.json
└── vite.config.ts

## 🔄 LLM Provider Routing

MeetingMind intelligently routes between LLM providers:

Upload Audio
↓
Check Ollama Available?
├─ YES → Use Ollama (Free, Local, Private)
└─ NO → Check Groq API Key?
├─ YES → Use Groq (Free Tier)
└─ NO → Error

**Benefits:**
- ✅ Zero API costs with Ollama
- ✅ Automatic fallback to Groq
- ✅ No vendor lock-in
- ✅ Switch providers anytime

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Audio Upload | 1-5s | Depends on file size |
| Transcription | 30-60s | 1-minute audio (~2-3x realtime) |
| AI Summarization | 5-10s | Using Groq/Ollama |
| Full Processing | 45-75s | Upload → Transcribe → Summarize |
| Batch Processing | 2-5min | 5 files in parallel |

## 🔐 Security

- ✅ No API keys in code (uses .env)
- ✅ CORS enabled for localhost development
- ✅ Input validation on all endpoints
- ✅ Secure audio file handling
- ✅ Database encryption ready

## 📈 Roadmap

### Phase 1 (Current)
- [x] Speech-to-text transcription
- [x] AI summarization
- [x] Export features
- [x] Dark mode
- [x] Batch processing

### Phase 2 (Planned)
- [ ] Speaker diarization (who said what)
- [ ] Multi-language support
- [ ] Real-time WebSocket updates
- [ ] AWS S3 integration
- [ ] Docker deployment

### Phase 3 (Future)
- [ ] Mobile app (React Native)
- [ ] Calendar integration
- [ ] Slack bot integration
- [ ] Email distribution
- [ ] Analytics dashboard

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Sathish Kumar Lingampelli**
- GitHub: [@sathishkumar-smart](https://github.com/sathishkumar-smart)
- Email: lingampellisathishkumar@gmail.com

## 🙏 Acknowledgments

- OpenAI Whisper for speech-to-text
- Groq for fast LLM inference
- Ollama for local LLM support
- FastAPI for the excellent framework
- React community for amazing tools

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/YOUR_USERNAME/meetingmind/issues)
- Start a [Discussion](https://github.com/YOUR_USERNAME/meetingmind/discussions)

---

**Made with ❤️ by Sathishkumar**

⭐ If this project helped you, please consider giving it a star!