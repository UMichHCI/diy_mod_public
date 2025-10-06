# DIY-MOD: Personalized Content Moderation Extension

DIY-MOD is a browser extension that empowers users to customize their online content experience through personalized content filtering. Using advanced LLM-powered content analysis, it provides flexible and context-aware content moderation that adapts to individual preferences.

## Features

- 🎯 **Personalized Filtering**: Create custom filters for specific topics, people, or concepts
- 🤖 **LLM-Powered Analysis**: Intelligent content understanding using GPT-4 models
- 🎚️ **Adjustable Intensity Levels**:
  - Low (< 3): Blur specific words
  - Medium (3): Add content warning overlays
  - High (> 3): AI-powered content rewriting
- 📱 **Multi-Content Support**: Filter both text and images
- ⏱️ **Temporal Controls**: Set filters for different durations (24 hours, 1 week, permanent)
- 💬 **Natural Language Interface**: Conversational setup of content filters
- 🖼️ **Image-Based Filter Creation**: Upload images to create filters based on visual content
- 🎨 **Visual Customization**:
  - Adjustable blur intensity and hover effects
  - Customizable warning overlays (dark/light themes)
  - Configurable border styles for modified content
  - Synchronized or independent border styling

## Architecture

### Browser Extension
- Content modification through DOM manipulation
- Real-time filter application
- User preference management
- Chat interface for filter configuration
- WebSocket connection for real-time updates

### Backend Server
- FastAPI-based REST API with async support
- LLM integration for content analysis and image understanding
- SQLite database for user preferences
- Content processing pipeline
- WebSocket support for real-time image processing
- Redis cache and Celery for async tasks

### Dual Feed Viewer (Frontend)
- Next.js application for side-by-side feed comparison
- Shows original content alongside filtered content
- JSON template system for testing custom feeds
- Real-time image processing updates via WebSocket
- Synchronized scrolling and hover interactions

## Setup

### Backend Setup
1. Create and activate a Python virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
cd Backend
pip install -r requirements.txt
```

3. Configure the application in `config.yaml`:
```yaml
llm:
  content_model: "gpt-4o-mini"
  filter_model: "gpt-4o"
  chat_model: "gpt-4o"
  temperature: 0.1
  max_tokens: 1000

processing:
  parallel_workers: 4
  cache_timeout: 60
  default_mode: "balanced"
  default_intensity: 3

# Optional: Configure default test filters
testing:
  create_default_filters: true
  default_filters:
    - filter_text: "Trump"
      content_type: "text"
      filter_type: "entity"
      intensity: 1
```

4. Optionally create a `.env` file to override configuration:
```
OPENAI_API_KEY=your-api-key-here
FILTER_CREATION_MODEL="gpt-4o"
CHAT_MODEL="gpt-4o"
CONTENT_PROCESS_MODEL="gpt-4o-mini"
PARALLEL_WORKERS=4
```

5. Start the backend services:
```bash
# Start Redis (required for caching)
redis-server

# Start the main API server
python app.py

# In another terminal, start Celery worker for image processing
celery -A CartoonImager worker --loglevel=info
```

### Performance Tuning
The backend server uses parallel processing to handle multiple posts simultaneously:
- `PARALLEL_WORKERS`: Controls the number of worker threads (default: 4)
- Processing is done in parallel using Python's ThreadPoolExecutor
- Each post's content is processed independently

### Browser Extension Setup
1. Build the extension:
```bash
cd BrowserExtension/modernized-extension
npm install
npm run build
```

2. Load in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `BrowserExtension/modernized-extension/dist` directory

### Dual Feed Viewer Setup
1. Install dependencies:
```bash
cd Frontend/dual-feed-viewer
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

### Quick Start (All Services)
For convenience, you can start all services at once:
```bash
./start-all.sh
```

This will start:
- Redis server
- Backend API (port 8001)
- Celery worker
- Dual Feed Viewer (port 3000)

To stop all services:
```bash
./stop-all.sh
```

## Usage

### Using the Browser Extension
1. Click the DIY-MOD extension icon
2. Describe what content you want to filter in natural language or upload an image
3. Configure filter settings:
   - Content type (text/images/both)
   - Intensity level (1-5)
   - Duration (temporary/permanent)
4. View and manage your filters through the extension interface

### Using the Dual Feed Viewer
1. Navigate to http://localhost:3000
2. Enter a JSON template with posts to process:
   - Mix Reddit URLs and custom posts
   - Specify intervention types for each post
3. Click "Process Feed" to see side-by-side comparison
4. Features:
   - Synchronized scrolling between original and filtered feeds
   - Real-time image processing updates
   - Hover highlighting of corresponding posts
   - Save processed feeds for later viewing

### Extension Settings
The extension provides detailed customization through its options page:
1. **Processing Mode**:
   - Balanced: Standard content filtering
   - Aggressive: Stricter filtering with lower thresholds

2. **Visual Settings**:
   - Blur intensity control (4-15px)
   - Content reveal on hover toggle
   - Border customization for warnings and rewrites
   - Dark/light overlay themes

3. **Filter Management**:
   - Import/export filter configurations
   - Bulk filter operations
   - Debug logging options

## Configuration
The application uses a robust configuration system:
- YAML-based configuration with environment variable overrides
- Pydantic models for type validation and defaults
- Section-specific configurations for LLM, processing, database, etc.
- Optional test filters for new users

See Backend/README.md for detailed configuration options
