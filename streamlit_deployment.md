# Streamlit Zoom Clone - Deployment Guide

## 📋 What Changed from Node.js Version?

### Original Node.js Architecture:
- **Port 3000**: Express.js server (handles Socket.io signaling)
- **Port 3001**: PeerJS server (manages WebRTC connections)
- **Files Required**:
  - `server.js` ✓ (Backend logic)
  - `public/script.js` (Frontend logic)
  - `views/room.ejs` (HTML template)
  - **ONLY `server.js` is NOT enough** - you need:
    - PeerJS server running (separate process on port 3001)
    - Both ports 3000 and 3001 must be exposed

### New Streamlit Architecture:
- **Single Application**: Python Streamlit app (handles everything)
- **Port 8501**: Streamlit development server (default)
- **Files Required**:
  - `streamlit_app.py` ✓ (All logic integrated)
  - `requirements.txt` ✓ (Python dependencies)
  - `.streamlit/config.toml` ✓ (Configuration)

---

## 🚀 Local Development (Port 8501)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run streamlit_app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://YOUR_IP:8501
```

### 3. Access the App
- Local: `http://localhost:8501`
- From another machine on same network: `http://YOUR_MACHINE_IP:8501`

---

## ☁️ Deploy to Streamlit Cloud

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Add Streamlit zoom clone"
git push origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Select branch: `main`
6. Set Main file path: `streamlit_app.py`
7. Click "Deploy"

**URL Pattern**: `https://[your-username]-[repo-name]-[random-id].streamlit.app`

### 3. Share with Others
- Share the Streamlit Cloud URL
- Each user gets their own room ID or can join existing rooms by entering room ID in sidebar

---

## 📊 Comparison: Node.js vs Streamlit

| Aspect | Node.js | Streamlit |
|--------|---------|----------|
| **Entry Point** | `node server.js` | `streamlit run streamlit_app.py` |
| **Ports Required** | 2 ports (3000 + 3001) | 1 port (8501) |
| **Deployment** | Heroku, AWS, DigitalOcean | Streamlit Cloud (FREE) |
| **Backend + Frontend** | Separate | Integrated |
| **Scaling** | Manual | Automatic on Streamlit Cloud |
| **Database** | Can add MongoDB/SQL | Use `st.session_state` or databases |
| **Cost (Cloud)** | Paid | Free tier available |

---

## ⚙️ Configuration Options

### Change Port (Local Only)
Edit `.streamlit/config.toml`:
```toml
[server]
port = 8501  # Change this
```

### Enable HTTPS (Recommended for Production)
```toml
[server]
sslCertFile = "/path/to/cert.pem"
sslKeyFile = "/path/to/key.pem"
```

---

## 🔗 Port Reference

| Scenario | Port | Usage |
|----------|------|-------|
| **Local Development** | `8501` | `streamlit run streamlit_app.py` |
| **Streamlit Cloud** | `N/A` | Provided by Streamlit (HTTPS) |
| **Docker Container** | `8501` | Internal port mapping |
| **Old Node.js** | `3000` | Express server |
| **Old Node.js** | `3001` | PeerJS server |

---

## 🐳 Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streamlit_app.py .
COPY .streamlit .streamlit

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

Run:
```bash
docker build -t zoom-clone .
docker run -p 8501:8501 zoom-clone
```

Then access: `http://localhost:8501`

---

## ✅ Verification Checklist

- [ ] Install Python 3.8+ (`python --version`)
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Run locally first (`streamlit run streamlit_app.py`)
- [ ] Test camera/microphone access
- [ ] Share room ID with other users
- [ ] Verify video streaming works
- [ ] Deploy to Streamlit Cloud
- [ ] Share Cloud URL with others

---

## 🆘 Troubleshooting

### "Port 8501 already in use"
```bash
streamlit run streamlit_app.py --server.port 8502
```

### "Camera access denied"
- Browser permissions: Check browser settings
- Windows: Settings > Privacy > Camera/Microphone
- Mac: System Preferences > Security & Privacy
- Linux: Install media plugins

### "Streamlit Cloud deployment fails"
- Check `requirements.txt` is in root directory
- Verify `streamlit_app.py` exists
- Check Python version compatibility
- Review deployment logs on Streamlit Cloud dashboard

---

## 📝 Key Differences from Original

| Feature | Original | Streamlit |
|---------|----------|-----------|
| Room ID | Passed via URL param | Displayed in sidebar |
| Video Grid | HTML/CSS grid | Streamlit WebRTC component |
| Drawing | Canvas API | HTML/JavaScript canvas |
| Messages | Socket.io events | Streamlit text input + session state |
| User List | Real-time updates | Sidebar display |
| Scaling | Requires server infrastructure | Streamlit Cloud handles it |

---

**Questions?** Check Streamlit docs: https://docs.streamlit.io/
