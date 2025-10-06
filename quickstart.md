# DIY-MOD Quick Start Guide

This repository contains the implementation for the paper:
**"What If Moderation Didn't Mean Suppression? A Case for Personalized Content Transformation"**
by Rayhan Rashed and Farnaz Jahanbakhsh
📄 Paper: https://arxiv.org/abs/2509.22861

## Prerequisites
- Python 3.8+
- Node.js 16+
- Redis server
- OpenAI API key (set in environment or config)

## Setup Instructions

### 1. Backend Setup
```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
cd Backend 
pip install -r requirements.txt

# Configure your API keys in Backend/config.yaml or create .env file
# OPENAI_API_KEY=your-api-key-here
```

### 2. Start Services
```bash
# Terminal 1: Start Redis server
redis-server

# Terminal 2: Start Celery workers for background tasks
cd Backend
source venv/bin/activate
celery -A celery_gevent_worker worker --loglevel=info -P gevent -c 1000

# Terminal 3: Start Backend API server
cd Backend
source venv/bin/activate
python app.py
# Server will run on http://localhost:8001
```

### 3. Browser Extension Setup
```bash
# Build the browser extension
cd BrowserExtension
npm install
npm run build

# Load extension in Chrome:
# 1. Open chrome://extensions/
# 2. Enable "Developer mode"
# 3. Click "Load unpacked"
# 4. Select the BrowserExtension/dist folder
```

### 4. Reddit Clone Frontend (Optional)
```bash
# Start the demo Reddit clone for testing
cd reddit-clone
npm install
npm run dev
# Frontend will run on http://localhost:3000
```

## Configuration

- **Server config**: `Backend/config.yaml`
- **Extension config**: `BrowserExtension/src/shared/config.ts`
- **Environment variables**: Create `.env` file in Backend directory

## Usage

### Create Custom Feed for Testing
```bash
cd Backend

# Create an example JSON feed
python process_json_custom_feed.py --create-example
# This creates example_mixed_feed.json

# Process the custom feed
python process_json_custom_feed.py custom_feed_example.json --save --user demo-user --title "Custom Feed Example"

# View processed feed at http://localhost:3000
```

### Using the Browser Extension
1. Click the DIY-MOD extension icon in your browser
2. Create filters using natural language or by uploading images
3. Configure filter intensity (1-5) and duration
4. Browse any website to see content transformation in action

## System Architecture
- **Backend**: FastAPI server with LLM integration and background processing [DIY-MOD Server]
- **Extension**: Content script that modifies web pages in real-time [DIY-MOD Client]
- **Frontend**: Next.js app for testing and feed comparison [Reddit Feed we use for User Study 2]
- **Processing**: Celery workers for handling image transformations [Async Image Transformation]

You are now ready to use the DIY-MOD system for personalized content moderation!

