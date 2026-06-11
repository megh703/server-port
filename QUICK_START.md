# 🚀 Quick Start Guide - Streamlit Zoom Clone

## Original Node.js Setup (What You Had)

```
server.js → Express (port 3000)
       ↓
   Socket.io (signaling)
       ↓
PeerJS Server (port 3001)
```

**Is `server.js` alone enough?** ❌ **NO**
- You NEED: `server.js` + PeerJS server running separately on port 3001
- You NEED: Both `port 3000` AND `port 3001` exposed in firewall

---

## New Streamlit Setup (Recommended)

```
streamlit_app.py → Single Application (port 8501)
       ↓
   Integrated Video + Chat + Canvas
```

**Is `streamlit_app.py` alone enough?** ✅ **YES**
- Only 1 file to run
- Only 1 port needed (8501)
- All logic self-contained

---

## 📥 Installation

```bash
# 1. Navigate to project
cd d:\Computervision\Zoom-Clone-With-WebRTC

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run streamlit_app.py
```

---

## 🎯 Usage

### Local (Development)
```
✓ Your machine: http://localhost:8501
✓ Other machines on network: http://YOUR_IP:8501
✓ Share Room ID from sidebar to let others join
```

### Streamlit Cloud (Production)
1. Push to GitHub
2. Deploy on https://share.streamlit.io
3. Share the generated URL (e.g., `https://your-name-zoom-clone.streamlit.app`)

---

## 📊 What's Equivalent?

| Node.js Port | Streamlit | Purpose |
|-------------|-----------|---------|
| `:3000` (Express) | `:8501` | Main application |
| `:3001` (PeerJS) | Built-in | Integrated in Streamlit |
| `/` route | Home page | Room creation |
| `/:room` | Sidebar info | Room display |

---

## ✅ Features Included

- ✓ Video streaming (multiple participants)
- ✓ Real-time audio
- ✓ Shared drawing canvas
- ✓ Message chat
- ✓ Room ID management
- ✓ User list display
- ✓ One-click room creation

---

## 🔧 Troubleshooting

**Problem**: Port 8501 already in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Problem**: Camera not working
- Windows: Settings → Privacy → Camera → Allow
- Firefox/Chrome: Grant permission in browser popup

**Problem**: Can't join room on different machine
- Ensure both on same network
- Use YOUR_IP (not localhost)
- Check Windows Firewall

---

## 📚 Next Steps

1. Run `streamlit run streamlit_app.py`
2. Share room ID with friends
3. Test video/audio
4. For production: Deploy to Streamlit Cloud
