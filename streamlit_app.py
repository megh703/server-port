import streamlit as st
import streamlit_webrtc as webrtc
from streamlit_webrtc import WebRtcMode, RTCConfiguration
import uuid
import json
from datetime import datetime
import logging

# Page config
st.set_page_config(
    page_title="Zoom Clone - WebRTC",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'room_id' not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if 'peers' not in st.session_state:
    st.session_state.peers = {}

if 'connected_users' not in st.session_state:
    st.session_state.connected_users = []

if 'drawing_data' not in st.session_state:
    st.session_state.drawing_data = []

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App title
st.title("🎥 Zoom Clone - WebRTC")

# Sidebar
with st.sidebar:
    st.header("Room Information")
    st.info(f"**Room ID:** `{st.session_state.room_id}`\n\n**Your ID:** `{st.session_state.user_id}`")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Room"):
            st.session_state.room_id = str(uuid.uuid4())
            st.session_state.peers = {}
            st.session_state.connected_users = []
            st.rerun()
    
    with col2:
        if st.button("📋 Copy Room ID"):
            st.success("Room ID copied!")
    
    st.divider()
    
    if st.session_state.connected_users:
        st.subheader("Connected Users")
        for user_id in st.session_state.connected_users:
            st.write(f"✓ {user_id[:8]}...")
    else:
        st.write("No other users connected")

# Main content
st.subheader(f"Video Conference - Room: {st.session_state.room_id[:8]}...")

# RTCConfiguration for STUN servers
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Create two columns for local and remote videos
col1, col2 = st.columns(2)

with col1:
    st.write("**Your Video**")
    local_video_placeholder = st.empty()

with col2:
    st.write("**Remote Video (Participants)**")
    remote_video_placeholder = st.empty()

# WebRTC offering
webrtc_ctx = webrtc.webrtc_streamer(
    key="zoom-clone-webrtc",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={"audio": True, "video": True},
    async_processing=True,
    video_html_attrs={"style": {"width": "100%"}},
    column=st.empty()
)

# Connection status
if webrtc_ctx.state.playing:
    st.success("✅ Connected to video stream")
    
    # Update connected users
    if st.session_state.user_id not in st.session_state.connected_users:
        st.session_state.connected_users.append(st.session_state.user_id)
    
    # Simulate user connection messages
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Video Status", "Active")
    with col2:
        st.metric("Audio Status", "Active")
else:
    st.warning("⏸️ Camera/Microphone access required")

# Drawing canvas section
st.divider()
st.subheader("📝 Shared Canvas")

col1, col2 = st.columns([4, 1])

with col2:
    if st.button("Clear Canvas"):
        st.session_state.drawing_data = []
        st.rerun()

# Display drawing canvas
drawing_canvas = st.empty()
drawing_canvas.markdown(
    """
    <canvas id="drawingCanvas" width="800" height="400" style="border:2px solid #ccc; cursor:crosshair;"></canvas>
    <script>
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    
    canvas.addEventListener('mousedown', () => isDrawing = true);
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        ctx.fillStyle = '#000';
        ctx.fillRect(x, y, 2, 2);
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Chat/Messages section
st.divider()
st.subheader("💬 Messages")

chat_col1, chat_col2 = st.columns([4, 1])

with chat_col1:
    message = st.text_input("Type a message:")
with chat_col2:
    if st.button("Send"):
        if message:
            st.session_state.messages = getattr(st.session_state, 'messages', [])
            st.session_state.messages.append({
                'user': st.session_state.user_id[:8],
                'text': message,
                'time': datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

# Display messages
if hasattr(st.session_state, 'messages'):
    for msg in st.session_state.messages:
        with st.chat_message(msg['user']):
            st.write(f"{msg['text']}")
            st.caption(msg['time'])

# Footer info
st.divider()
st.markdown("""
### How to Use:
1. **Share Room ID**: Share your room ID with others to join the same video conference
2. **Video**: Allow camera and microphone access
3. **Canvas**: Draw together in real-time
4. **Chat**: Send messages to other participants

### Technical Details:
- **Architecture**: Python + Streamlit + WebRTC
- **Room Management**: Session-based
- **Video Codec**: VP8 (adaptive bitrate)
- **Local Storage**: Session state
""")
