# DIY-MOD: Personalized Content Moderation System

This repository contains the implementation for the paper:


**What If Moderation Didn't Mean Suppression? A Case for Personalized Content Transformation**
Rayhan Rashed and Farnaz Jahanbakhsh
📄 Paper Link: [https://arxiv.org/abs/2509.22861](https://arxiv.org/abs/2509.22861)

## What is DIY-MOD?

DIY-MOD is a browser extension that lets users personalize their online content experience. Instead of simply blocking unwanted content, it transforms it using AI - blurring, adding warnings, or rewriting content based on your preferences.

## System Components

### Core DIY-MOD System (Main Implementation)
- **Backend**: AI-powered content processing server
- **Browser Extension**: Real-time content transformation in your browser

### User Study Components (Research Tools)
- **Reddit Clone**: Custom frontend used for User Study 2 to test feed comparison
- **Custom Feed Tools**: Scripts for creating test feeds with controlled content

## Prerequisites
- Python 3.8+
- Node.js 16+
- Redis server
- OpenAI and Gemini API key(s)

## Quick Start: Core DIY-MOD System

### 1. Backend Setup
```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
cd Backend 
pip install -r requirements.txt

# Configure your API key in Backend/config.yaml or create .env file
# OPENAI_API_KEY=your-api-key-here
```

### 2. Start the Backend Services
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

### 3. Install Browser Extension
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

## Using DIY-MOD

Once installed, you can:

1. **Click the DIY-MOD extension icon** in your browser toolbar
2. **Create content filters** using natural language (e.g., "blur political content") or by uploading example images
3. **Set filter intensity** (1-5): from subtle blurring to complete content rewriting
4. **Choose duration**: temporary (24 hours) or permanent filters
5. **Browse any website** - DIY-MOD will automatically transform content based on your filters

The extension currently works on top of Reddit and transforms content in real-time as you browse.
Twitter and Facebook support is coming!!

## Configuration

- **Backend settings**: `Backend/config.yaml`
- **Extension settings**: Available through the extension's options page
- **API keys**: Set `OPENAI_API_KEY` in environment or config file

## For Researchers: User Study Tools

If you want to replicate our user study or test custom feeds:

### Reddit Clone (User Study 2 Tool)
```bash
# Start the research frontend
cd reddit-clone
npm install
npm run dev
# Runs on http://localhost:3000
```

### Custom Feed Testing
```bash
cd Backend

# Create test feed data
python process_json_custom_feed.py --create-example

# Process custom feeds for comparison
python process_json_custom_feed.py custom_feed_example.json --save --user demo-user --title "Test Feed"

# View processed feeds in reddit-clone frontend
```

The reddit-clone frontend shows side-by-side comparisons of original vs. transformed content, which was used in our research to evaluate user preferences.

## System Architecture

- **Backend Server**: FastAPI with LLM integration for content analysis and transformation
- **Browser Extension**: Content script that modifies web pages in real-time
- **Celery Workers**: Background processing for image transformations
- **Redis Cache**: Fast caching for processed content
- **Reddit Clone**: Research tool for controlled feed comparison studies

You are now ready to use DIY-MOD for personalized content moderation!

