# WebRTC Zoom Clone - Deployment & Connection Guide

## Part 1: Deploy Node.js Signaling Server to Render (Free Cloud)

### Step 1.1: Prepare GitHub Repository
1. **Commit your code:**
   ```bash
   cd d:\Computervision\Zoom-Clone-With-WebRTC
   git add .
   git commit -m "Prepare for cloud deployment: Add Procfile and start script"
   git push origin main
   ```

2. **Verify these files are in your repository:**
   - `server.js` (main signaling server)
   - `package.json` (with start script)
   - `Procfile` (newly added)
   - `views/` directory
   - `public/` directory

### Step 1.2: Deploy to Render
1. **Create Render account:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository containing this code
   - Select the repository

3. **Configure deployment:**
   - **Name:** `zoom-clone-signaling` (or any name)
   - **Environment:** Node
   - **Build Command:** `npm install`
   - **Start Command:** `node server.js`
   - **Plan:** Free tier (sufficient for testing)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - You'll see a green checkmark when complete

5. **Get your Deployed URL:**
   - Copy the URL shown on the Render dashboard
   - Example: `https://zoom-clone-signaling.onrender.com`
   - **SAVE THIS URL** - you'll need it for Android and Streamlit

### Step 1.3: Verify Deployment
1. Open the deployed URL in your browser
2. You should see the Zoom Clone UI (if you're running on the web client)
3. Check Render logs to confirm: `Signaling server listening on port 3000`

---

## Part 2: Update Android App to Use Deployed Server

### Step 2.1: Update SignalingConfig
1. **Open file:**
   ```
   C:\Users\meghana.v\AndroidStudioProjects\extracted\ARAssistant\app\src\main\java\com\example\arassistant\network\SignalingConfig.kt
   ```

2. **Replace the URL (replace `YOUR_DEPLOYED_URL` with your Render URL):**
   ```kotlin
   object SignalingConfig {
       const val DEFAULT_SERVER_URL = "https://zoom-clone-signaling.onrender.com"  // ← Update this
       const val DEFAULT_ROOM_ID = "ar-session"
   }
   ```

3. **Example - if your Render URL is:**
   ```
   https://my-awesome-server.onrender.com
   ```
   **Then use:**
   ```kotlin
   const val DEFAULT_SERVER_URL = "https://my-awesome-server.onrender.com"
   ```

### Step 2.2: Rebuild Android App
1. **In Android Studio:**
   - Click Build → Rebuild Project
   - Wait for build to complete

2. **Run on physical devices:**
   - Connect two Android phones via USB (or use Android emulator)
   - Press Run (or Shift + F10)
   - App will install and launch on both phones

---

## Part 3: Update Streamlit App

### Step 3.1: Fix streamlit_app.py
Replace the content of `d:\Computervision\Zoom-Clone-With-WebRTC\streamlit_app.py` with:

```python
import streamlit as st
import uuid

# Page config
st.set_page_config(page_title="Zoom Clone Control", layout="wide")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "room_id" not in st.session_state:
    st.session_state.room_id = "ar-session"

# ===== REPLACE THIS WITH YOUR DEPLOYED SERVER URL =====
DEPLOYED_SERVER_URL = "https://zoom-clone-signaling.onrender.com"
# ======================================================

# Title
st.title("🎥 WebRTC Zoom Clone - Connection Control")

# Sidebar: Connection Info
with st.sidebar:
    st.header("📡 Server Configuration")
    st.write(f"**Server URL:**")
    st.code(DEPLOYED_SERVER_URL, language="text")
    
    st.write(f"**Your User ID:**")
    st.code(st.session_state.user_id, language="text")
    
    st.write(f"**Current Room:**")
    st.session_state.room_id = st.text_input("Room ID", value=st.session_state.room_id)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 Connection Instructions")
    st.markdown("""
    ### For Two-Phone Connection:
    
    **Phone 1 (Device A):**
    1. Open ARAssistant app
    2. Tap "Assistant" or "Engineer"
    3. In Join Activity, clear the Server URL field
    4. Paste this server URL:
    """)
    st.code(DEPLOYED_SERVER_URL, language="text")
    st.markdown(f"""
    5. Enter Room ID: `{st.session_state.room_id}`
    6. Tap "Join Session"
    
    **Phone 2 (Device B):**
    1. Repeat the same steps (1-6) on the second phone
    2. Use the **SAME** Room ID as Device A
    3. Both phones should discover each other and connect
    
    """)

with col2:
    st.subheader("✅ Connection Status")
    st.markdown("""
    **Status Indicators:**
    - 🟢 Green: Connected to signaling server
    - 🔴 Red: Not connected (check server URL)
    
    **To test connection:**
    1. Start app on Phone 1
    2. Open browser to deployed server URL (optional)
    3. Start app on Phone 2
    4. Both should appear in the same room
    5. Video/audio should stream between phones
    """)

# Footer
st.markdown("---")
st.markdown("""
**Server Status:** Your signaling server is running at the URL shown above.  
Update `DEPLOYED_SERVER_URL` in this file when you deploy to a new server.
""")
```

### Step 3.2: Deploy Updated Streamlit App

1. **Commit changes:**
   ```bash
   cd d:\Computervision\Zoom-Clone-With-WebRTC
   git add streamlit_app.py
   git commit -m "Update Streamlit app with deployed server URL and connection instructions"
   git push
   ```

2. **Redeploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo and `streamlit_app.py`
   - Streamlit will automatically redeploy

---

## Part 4: Step-by-Step Connection Procedure

### Prerequisites
- **Two Android phones** (or emulators)
- **Deployed Node.js server URL** (from Part 1.3)
- **Both apps updated** (Android app updated to use deployed URL, Streamlit updated with instructions)

### Connection Steps

#### Step A: Prepare Phone 1 (Assistant)
1. **Launch the ARAssistant app on Phone 1**
2. **Tap "Assistant"** (or "Engineer" if you prefer)
3. **In the Join Activity screen:**
   - Server URL field should auto-populate with the deployed server URL
   - If not, clear it and paste: `https://zoom-clone-signaling.onrender.com` (replace with your URL)
   - Room ID: Use default `ar-session` or enter your custom room name
4. **Tap "Join Session"**
5. **Allow permissions** when prompted (camera, microphone, etc.)
6. **Keep the app open** - you should see your own video feed

#### Step B: Prepare Phone 2 (Engineer)
1. **Launch the ARAssistant app on Phone 2**
2. **Tap "Engineer"** (or "Assistant" - can mix and match)
3. **In the Join Activity screen:**
   - Use the **EXACT SAME** server URL as Phone 1
   - Use the **EXACT SAME** room ID as Phone 1 (e.g., `ar-session`)
4. **Tap "Join Session"**
5. **Allow permissions** when prompted
6. **Both phones should now be connected:**
   - Phone 1 should see Phone 2's video feed
   - Phone 2 should see Phone 1's video feed
   - Drawing data should sync between devices

#### Step C: Verify Connection Success
- ✅ Both phones are in the same room
- ✅ Video feeds are visible on both devices
- ✅ Drawing/annotations sync between phones
- ✅ Audio/video latency is minimal

### Troubleshooting

| Problem | Solution |
|---------|----------|
| **Phones not connecting** | 1. Verify both use SAME room ID. 2. Check server URL is correct. 3. Restart both apps. |
| **"Connection refused" error** | Check that Render server is running (green status on dashboard). Redeploy if needed. |
| **Video not appearing** | Grant camera permissions. Restart app. Check internet connection. |
| **High latency** | Normal for cloud signaling. Reduce video resolution in app settings if available. |
| **Disconnects frequently** | Check WiFi signal strength. Move closer to router. Reduce background apps. |

---

## Part 5: Optional - Deploy Streamlit App to Streamlit Cloud

If you want your Streamlit UI hosted online:

1. **Go to https://share.streamlit.io**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select:**
   - Repository: Your GitHub repo
   - Branch: `main`
   - File: `streamlit_app.py`
5. **Streamlit automatically deploys**
6. **Share the public Streamlit URL** with anyone who wants to monitor connections

---

## Summary

Your system architecture is now:
```
Phone 1 (Assistant) ─┐
                      ├─→ [Deployed Node.js Server on Render] ←─ Streamlit Web UI
Phone 2 (Engineer)   ─┘      (https://zoom-clone-signaling.onrender.com)
```

- **Node.js Server:** Manages room signaling and WebRTC negotiation
- **Android Phones:** Join room via SignalingConfig URL, exchange WebRTC offers/answers
- **Streamlit:** Shows server URL and connection instructions (optional, for monitoring)

---

## Next Steps

1. ✅ Deploy Node.js to Render (Part 1)
2. ✅ Update Android app (Part 2)
3. ✅ Update Streamlit (Part 3)
4. ✅ Test two-phone connection (Part 4)
5. (Optional) Deploy Streamlit to Streamlit Cloud (Part 5)

Once you complete Parts 1-3, you're ready to connect two phones!

---

**Questions?**
- Check Render logs at: https://dashboard.render.com
- Check Streamlit logs at: https://share.streamlit.io
- Verify SignalingConfig.kt points to your deployed URL
