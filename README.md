# CaseConnect

A semantic search system for legal case analysis across multiple jurisdictions.

## Features

- Multi-jurisdictional case search
- Semantic similarity analysis
- Cross-lingual support
- Interactive user interface
- Temporal analysis capabilities

## Prerequisites

- Docker
- Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Bananito96/CaseConnect.git
cd case-connect
```

2. Start the services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Documentation: http://localhost:5000/docs

## Development Setup

### Frontend

```bash
cd frontend
npm install
npm start
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
flask run
```

## Deployment

For production deployment:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Project Structure

```
case-connect/
├── frontend/          # React application
├── backend/           # Flask API
├── data/             # Embedding data
└── scripts/          # Utility scripts
```

## License

MIT

## Authors
- Simone Vagnoni - Simone.vagnoni3@unibo.it
- Coco Cesara Lois Arden Krumsick - coco.krumsick@studio.unibo.it 
- Leonardo Zilli - leonardo.zilli@studio.unibo.it
- Lou- Anne Olivier - olivier.louanne@studio.unibo.it
