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

