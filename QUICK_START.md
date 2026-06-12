# Quick Start: Connect Two Android Phones via Cloud Server

## 🚀 Overview
Your two Android phones will connect through a deployed Node.js signaling server (running on Render Cloud). The Streamlit app shows the connection configuration.

---

## ⚡ Phase 1: Deploy Server (5 minutes)

### 1.1 Push code to GitHub
```bash
cd d:\Computervision\Zoom-Clone-With-WebRTC
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 1.2 Deploy to Render
1. Go to **https://render.com**
2. Sign up with GitHub
3. Click **"New +" → "Web Service"**
4. Connect your repository with the code
5. Set up:
   - **Name:** `zoom-clone-signaling`
   - **Build Command:** `npm install`
   - **Start Command:** `node server.js`
   - **Plan:** Free
6. Click **"Create Web Service"** and wait 2-3 minutes

### 1.3 Get your server URL
- Render dashboard shows your URL (e.g., `https://zoom-clone-signaling.onrender.com`)
- **SAVE THIS URL** ← You'll need it below

---

## ⚡ Phase 2: Update Android App (2 minutes)

### 2.1 Update server URL
File: `C:\Users\meghana.v\AndroidStudioProjects\extracted\ARAssistant\app\src\main\java\com\example\arassistant\network\SignalingConfig.kt`

Replace:
```kotlin
const val DEFAULT_SERVER_URL = "https://zoom-clone-signaling.onrender.com"
```

With your actual Render URL (from Phase 1.3).

### 2.2 Rebuild
- In Android Studio: **Build → Rebuild Project**

---

## ⚡ Phase 3: Update Streamlit (1 minute)

### 3.1 Update server URL
File: `d:\Computervision\Zoom-Clone-With-WebRTC\streamlit_app.py`

Replace line 14:
```python
DEPLOYED_SERVER_URL = "https://zoom-clone-signaling.onrender.com"
```

With your actual Render URL.

### 3.2 Commit
```bash
cd d:\Computervision\Zoom-Clone-With-WebRTC
git add streamlit_app.py
git commit -m "Update with deployed server URL"
git push
```

---

## ⚡ Phase 4: Connect Two Phones (5 minutes)

### Phone 1 (First Device)
1. Install and launch **ARAssistant** app
2. Tap **"Assistant"** or **"Engineer"**
3. Join Activity screen auto-fills with server URL and room ID
4. Tap **"Join Session"**
5. **Allow camera/microphone permissions**
6. Keep app open → you see your camera feed

### Phone 2 (Second Device)
1. Install and launch **ARAssistant** app
2. Tap **"Assistant"** or **"Engineer"** (can be different role than Phone 1)
3. **SAME server URL** as Phone 1 (should auto-fill)
4. **SAME room ID** as Phone 1 (default: `ar-session`)
5. Tap **"Join Session"**
6. **Allow camera/microphone permissions**

### ✅ Connection Success!
Both phones will now:
- 🎥 See each other's video feeds
- 🖌️ Share drawing/annotation data
- 🔊 Exchange audio (if WebRTC audio configured)
- 📍 Work over the internet via deployed server

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| Phones not connecting | 1. Check both use SAME room ID. 2. Verify server URL is correct. 3. Restart both apps. |
| "Connection refused" | Verify Render server has green status on dashboard. Restart if needed. |
| No video | Grant camera permission. Restart app. Check internet. |
| Frequent disconnects | Check WiFi signal. Move closer to router. Restart app. |

---

## 📋 What Changed

### Created/Updated Files:
✅ `Procfile` - Deploy config for Render  
✅ `package.json` - Added start script  
✅ `streamlit_app.py` - Simplified UI with server URL display  
✅ `SignalingConfig.kt` - Updated to deployed server URL  
✅ `DEPLOYMENT_GUIDE.md` - Full detailed guide  

### Architecture:
```
┌─────────────┐
│   Phone 1   │
│ (Assistant) │
└──────┬──────┘
       │
       ├──→ [Deployed Node.js Server] ←─ Streamlit Web UI
       │        on Render Cloud         (shows connection info)
┌──────┴──────┐
│   Phone 2   │
│  (Engineer) │
└─────────────┘
```

---

## ✨ Next (Optional)

Want your Streamlit UI on the internet too?
1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Deploy `streamlit_app.py` from your repo
4. Get public Streamlit URL for monitoring

---

## 📞 Support

- **Server not starting?** Check Render logs at: https://dashboard.render.com
- **Port issues?** Render automatically assigns the correct port
- **WebRTC offers/answers not working?** Check server.js Socket.io event handlers are firing (check Render console logs)

---

**You're ready! Follow phases 1-4 in order and you'll have two phones talking to each other.** 🎉
