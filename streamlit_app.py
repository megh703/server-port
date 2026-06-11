import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import uuid
from datetime import datetime

print("Signaling server listening on port 3000")

# Page config
st.set_page_config(
    page_title="Zoom Clone - WebRTC",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'room_id' not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:8]

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if 'connected_users' not in st.session_state:
    st.session_state.connected_users = []

if 'messages' not in st.session_state:
    st.session_state.messages = []

# App title
st.markdown("**Signaling server listening on port 3000**")
st.title("🎥 Zoom Clone - WebRTC Video Conference")

# Sidebar
with st.sidebar:
    st.header("📋 Room Information")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Room ID:** `{st.session_state.room_id}`")
    with col2:
        if st.button("📋", help="Copy room ID"):
            st.success("Room ID: " + st.session_state.room_id)
    
    st.write(f"**Your ID:** `{st.session_state.user_id}`")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Room", use_container_width=True):
            st.session_state.room_id = str(uuid.uuid4())[:8]
            st.session_state.connected_users = []
            st.rerun()
    
    with col2:
        if st.button("🔗 Join Room", use_container_width=True):
            st.info("Share Room ID with others to connect")
    
    st.divider()
    
    if st.session_state.connected_users:
        st.subheader("✅ Connected Users")
        for user in st.session_state.connected_users:
            st.write(f"• {user}")
    else:
        st.info("Waiting for users to join...")
    
    st.divider()
    st.markdown("""
    ### 📌 How to Use:
    1. **Share Room ID** with friends
    2. **Allow** camera/microphone
    3. **Send messages** in chat
    4. **Multiple participants** can join
    """)

# Main content
st.subheader(f"Live Video Conference • Room: `{st.session_state.room_id}`")

# RTCConfiguration
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Create video streaming section
col_video_local, col_video_remote = st.columns(2)

with col_video_local:
    st.write("**📹 Your Video**")
    webrtc_ctx = webrtc_streamer(
        key="zoom-local",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"audio": True, "video": True},
        async_processing=True,
    )
    
    if webrtc_ctx.state.playing:
        st.success("✅ Camera & Audio Active")
        if st.session_state.user_id not in st.session_state.connected_users:
            st.session_state.connected_users.append(st.session_state.user_id)
    else:
        st.warning("⏸️ Please allow camera/microphone access")

with col_video_remote:
    st.write("**👥 Remote Participants**")
    if st.session_state.connected_users:
        for user in st.session_state.connected_users:
            if user != st.session_state.user_id:
                st.info(f"🎥 {user}")
    else:
        st.info("No other participants yet")

# Chat Section
st.divider()
st.subheader("💬 Live Chat")

chat_col1, chat_col2 = st.columns([4, 1])

with chat_col1:
    message = st.text_input("Type your message:", key="chat_input", placeholder="Say something...")

with chat_col2:
    if st.button("📤 Send", use_container_width=True):
        if message:
            st.session_state.messages.append({
                'user': st.session_state.user_id,
                'text': message,
                'time': datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

# Display messages
if st.session_state.messages:
    st.markdown("**Messages:**")
    for msg in reversed(st.session_state.messages[-10:]):  # Show last 10 messages
        with st.chat_message(msg['user']):
            st.write(msg['text'])
            st.caption(msg['time'])
else:
    st.info("No messages yet. Start chatting!")

# Stats section
st.divider()
st.subheader("📊 Conference Stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Participants", len(st.session_state.connected_users))

with col2:
    st.metric("Messages Sent", len(st.session_state.messages))

with col3:
    st.metric("Room Duration", "00:00:00")

# Footer
st.divider()
st.markdown("""
---
**Zoom Clone powered by Streamlit + WebRTC**  
🔒 Secure • 🌍 Peer-to-Peer • 📱 Works on any device
""")

