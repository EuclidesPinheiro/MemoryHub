# MemoryHub 🧠

A modern memory management dashboard for AI applications. Built with **Python + FastAPI**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- 📊 **Memory Explorer** - List, search, and filter stored memories
- ⚡ **Playground** - Create new memory items with custom tags and TTL
- 📖 **API Documentation** - Built-in Swagger UI and ReDoc
- 🗄️ **SQLite Persistence** - Reliable local database storage
- 🎨 **Modern Dark UI** - Beautiful, responsive design

## Quick Start

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/EuclidesPinheiro/MemoryHub.git
cd MemoryHub

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Open your browser at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/memories` | Create a new memory |
| `GET` | `/api/memories` | List all memories |
| `GET` | `/api/memories/{id}` | Get a specific memory |
| `DELETE` | `/api/memories/{id}` | Delete a memory |

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
MemoryHub/
├── main.py           # FastAPI application
├── models.py         # Pydantic models
├── database.py       # SQLite operations
├── requirements.txt  # Python dependencies
├── templates/        # Jinja2 HTML templates
│   ├── base.html
│   ├── explorer.html
│   ├── playground.html
│   └── docs.html
└── static/
    └── styles.css    # CSS styles
```

