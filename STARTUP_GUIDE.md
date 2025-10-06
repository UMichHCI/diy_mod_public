# DIY-MOD Complete Startup Guide

## Prerequisites
- Python 3.11+ installed
- Node.js and npm installed  
- Redis installed (`brew install redis` on macOS)
- Chrome browser for extension testing

## Terminal Setup Overview
You'll need **5 terminal windows** total:
1. **Terminal 1**: Backend services (using startup script)
2. **Terminal 2**: Reddit Clone frontend  
3. **Terminal 3**: Browser Extension dev build
4. **Terminal 4**: Monitor logs (optional)
5. **Terminal 5**: General commands

---

## Step-by-Step Instructions

### Terminal 1: Start All Backend Services

```bash
# Navigate to backend directory
cd /Users/academics/Desktop/DIY_Mod/Backend

# Make scripts executable (first time only)
chmod +x start_all_services.sh stop_all_services.sh

# Start all backend services
./start_all_services.sh
```

This will start:
- Redis (port 6379)
- Main Backend API (port 8001) - for browser extension
- Reddit Clone Backend API (port 8002) - for dual feed viewer  
- Celery Worker - for image processing

**Expected output:**
```
✅ All backend services started!

Service Status:
- Redis: Port 6379
- Main Backend (Browser Extension): http://localhost:8001
- Reddit Clone Backend: http://localhost:8002
- Celery Worker: Running
```

**Keep this terminal open** - it shows logs from all backend services

### Terminal 2: Start Reddit Clone Frontend

```bash
# Navigate to reddit clone directory
cd /Users/academics/Desktop/DIY_Mod/reddit-clone

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

**Expected output:**
```
> reddit-clone@0.1.0 dev
> next dev

- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Keep this terminal open** - it shows frontend logs

### Terminal 3: Start Browser Extension

```bash
# Navigate to browser extension directory
cd /Users/academics/Desktop/DIY_Mod/BrowserExtension/modernized-extension

# Install dependencies (first time only)
npm install

# Start development build with hot reload
npm run dev
```

**Expected output:**
```
VITE v5.x.x ready in xxx ms
➜ Local: http://localhost:5173/
➜ press h + enter to show help
```

**Keep this terminal open** - it rebuilds extension on file changes

### Terminal 4: Monitor Logs (Optional)

```bash
# Navigate to backend directory
cd /Users/academics/Desktop/DIY_Mod/Backend

# Watch backend logs
tail -f *.log

# Or watch specific logs
tail -f app_main.log    # Main backend logs
tail -f app_reddit.log  # Reddit clone backend logs
```

### Terminal 5: Verify Services & General Commands

```bash
# Check if all services are running properly

# Test main backend (browser extension API)
curl http://localhost:8001/filters?user_id=test-user

# Test reddit clone backend
curl http://localhost:8002/health

# Test reddit clone frontend
curl http://localhost:3000

# Expected responses:
# Main backend: JSON with filters array
# Reddit backend: {"status":"healthy","service":"reddit-clone-backend","port":8002,...}
# Frontend: HTML page content
```

---

## Loading the Browser Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **"Developer mode"** toggle (top right corner)
3. Click **"Load unpacked"** button
4. Navigate to: `/Users/academics/Desktop/DIY_Mod/BrowserExtension/modernized-extension/dist`
5. Select the `dist` folder and click **"Open"**
6. The DIY-MOD extension should appear in your extensions list
7. Pin the extension to your toolbar for easy access

**Note**: After running `npm run dev` in Terminal 3, the `dist` folder is automatically updated when you make changes

---

## Testing the System

### Test Browser Extension:
1. Navigate to Reddit (reddit.com) or Twitter (x.com)
2. Click the DIY-MOD extension icon in toolbar
3. Configure content filters
4. Watch real-time content filtering on the page

### Test Reddit Clone Viewer:
1. Open http://localhost:3000 in your browser
2. You should see the dual feed interface
3. Select feeds from the dropdown menu
4. View original vs filtered content side-by-side

### Test WebSocket Connections:
- Open browser DevTools (F12) on either site
- Go to Network tab → WS (WebSocket)
- You should see active WebSocket connections

---

## Stopping All Services

### Method 1: Using Stop Script (Recommended)
In any terminal:
```bash
cd /Users/academics/Desktop/DIY_Mod/Backend
./stop_all_services.sh
```

### Method 2: Manual Stop
- **Terminal 1**: Press `Ctrl+C` to stop backend services
- **Terminal 2**: Press `Ctrl+C` to stop Reddit Clone frontend
- **Terminal 3**: Press `Ctrl+C` to stop Browser Extension dev server
- **Stop Redis** (if needed): `redis-cli shutdown`

---

## Service Port Reference

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Redis | 6379 | redis://localhost:6379 | Caching & task queue |
| Main Backend | 8001 | http://localhost:8001 | Browser extension API |
| Reddit Clone Backend | 8002 | http://localhost:8002 | Dual feed viewer API |
| Reddit Clone Frontend | 3000 | http://localhost:3000 | Dual feed viewer UI |
| Extension Dev Server | 5173 | http://localhost:5173 | Hot reload for extension |

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port (replace PORT with actual port number)
lsof -i :PORT

# Kill process using port
lsof -ti:PORT | xargs kill

# Example for port 8001
lsof -ti:8001 | xargs kill
```

### Redis Connection Refused
```bash
# Check if Redis is running
redis-cli ping

# Start Redis manually
redis-server

# Or on macOS with Homebrew
brew services start redis
```

### Python Dependencies Missing
```bash
cd /Users/academics/Desktop/DIY_Mod/Backend
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### Extension Not Updating
1. Go to `chrome://extensions/`
2. Click the refresh icon on DIY-MOD extension
3. Or disable/enable the extension

### WebSocket Connection Failed
1. Ensure all backend services are running
2. Check browser console for errors
3. Verify CORS settings in backend

---

## Development Tips

### Hot Reload
- **Browser Extension**: Changes auto-rebuild with `npm run dev`
- **Reddit Clone Frontend**: Next.js auto-reloads on file changes
- **Backend**: Restart required for Python changes (Ctrl+C then restart)

### Viewing Logs
- **Backend logs**: Appear in Terminal 1
- **Frontend logs**: Check browser DevTools Console
- **Extension logs**: Background script logs in extension's "Inspect views"

### Database
- SQLite database location: `/Users/academics/Desktop/DIY_Mod/Backend/diy_mod.db`
- View with: `sqlite3 diy_mod.db` then `.tables` and `.schema`

---

## Quick Start (Copy-Paste Commands)

### First Time Setup
```bash
# Terminal 1
cd /Users/academics/Desktop/DIY_Mod/Backend
chmod +x start_all_services.sh stop_all_services.sh
./start_all_services.sh

# Terminal 2
cd /Users/academics/Desktop/DIY_Mod/reddit-clone
npm install
npm run dev

# Terminal 3
cd /Users/academics/Desktop/DIY_Mod/BrowserExtension/modernized-extension
npm install
npm run dev
```

### Daily Startup
```bash
# Terminal 1
cd /Users/academics/Desktop/DIY_Mod/Backend && ./start_all_services.sh

# Terminal 2
cd /Users/academics/Desktop/DIY_Mod/reddit-clone && npm run dev

# Terminal 3
cd /Users/academics/Desktop/DIY_Mod/BrowserExtension/modernized-extension && npm run dev
```

---

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Browser + Ext   │────▶│ Main Backend    │────▶│     Redis       │
│                 │     │ (Port 8001)     │     │  (Port 6379)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
┌─────────────────┐     ┌─────────────────┐              │
│ Reddit Clone UI │────▶│ Reddit Backend  │──────────────┘
│ (Port 3000)     │     │ (Port 8002)     │
└─────────────────┘     └─────────────────┘
                                                          │
                        ┌─────────────────┐              │
                        │ Celery Workers  │──────────────┘
                        │ (Image Process) │
                        └─────────────────┘
```

Each component runs independently and communicates via HTTP/WebSocket.