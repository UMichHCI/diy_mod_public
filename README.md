# DIY-MOD: Personalized Content Moderation System

This repository contains the official implementation for the paper:

**What If Moderation Didn't Mean Suppression? A Case for Personalized Content Transformation**  
*Rayhan Rashed and Farnaz Jahanbakhsh*  
📄 [Read the Paper](https://arxiv.org/abs/2509.22861) | 🌐 [Project Website](https://rayhan.io/diymod/)

## Overview

**DIY-MOD** is an end-to-end system that enables users to personalize their online content experience without platform-side censorship. Instead of simply blocking unwanted content, DIY-MOD transforms it using Large Language Models (LLMs)—applying interventions such as blurring, warning labels, or content rewriting based on user-defined natural language preferences.

## System Architecture

The system consists of two primary components:

1.  **Core DIY-MOD System**:
    *   **Backend**: A Python/FastAPI server that handles content processing, LLM interaction, and caching.
    *   **Browser Extension**: A Chrome extension that intercepts web content and applies real-time transformations.

2.  **Research Tools**:
2.  **Research Tools**:
    *   **Dual-Feed System** (Section 6): A controlled simulation used in our user studies. [Live Demo](https://diy-mod.vercel.app/) | [Readme](reddit-clone/README.md)

## Prerequisites

*   **Python**: 3.8+
*   **Node.js**: 16+
*   **Redis**: Required for task queue and caching.
*   **API Keys**: OpenAI (GPT-4o/GPT-4o-mini) and Google Gemini (for image processing).

## Quick Start

### 1. Backend Setup

The backend handles the heavy lifting of content analysis and transformation.

```bash
# 1. Clone the repository and navigate to Backend
cd Backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Environment Variables
cp .env.template .env
# Open .env and add your OpenAI and Google API keys
```

### 2. Start Services

You will need to run the Redis server, Celery workers, and the API server simultaneously.

**Terminal 1: Redis**
```bash
redis-server
```

**Terminal 2: Celery Worker**
```bash
cd Backend
source venv/bin/activate
# Using gevent for concurrent task handling
celery -A celery_gevent_worker worker --loglevel=info -P gevent -c 1000
```

**Terminal 3: API Server**
```bash
cd Backend
source venv/bin/activate
python app.py
# Server will start at http://localhost:8001
```

### 3. Browser Extension Setup

```bash
cd BrowserExtension
npm install
npm run build
```

**To Load in Chrome:**
1.  Navigate to `chrome://extensions/`.
2.  Enable **Developer mode** (toggle in top-right).
3.  Click **Load unpacked**.
4.  Select the `BrowserExtension/dist` directory.

## Configuration

*   **Backend Config**: Main settings are in `Backend/config.yaml`.
*   **Environment Variables**: API keys and secrets are managed in `Backend/.env`.
*   **Extension Settings**: Configurable via the extension's popup interface.

## Research & User Study Tools

To replicate our study environment or test with the Reddit Clone:

### Reddit Clone Interface

This custom frontend interacts with the DIY-MOD backend to display transformed feeds side-by-side with original content.

```bash
cd reddit-clone

# Install dependencies
npm install

# Setup Environment
# Create .env.local if not present (see .env.production for reference keys)

# Start Development Server
npm run dev
# Access at http://localhost:3000
```

### Creating Custom Feeds

We provide scripts to generate and process custom feeds for testing:

```bash
cd Backend
# Create example feed data
python process_json_custom_feed.py --create-example

# Process the feed using the DIY-MOD pipeline
python process_json_custom_feed.py custom_feed_example.json --save --user demo-user --title "Test Feed"
```

## License

[MIT License](LICENSE)
