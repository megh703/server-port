import streamlit as st
import uuid

st.set_page_config(
    page_title="Camera Preview",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "room_id" not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:8]

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

st.title("📹 Camera Preview")
st.caption("This page opens the browser camera directly from the Streamlit URL, similar to the old localhost page.")

with st.sidebar:
    st.header("Room Info")
    st.text_input("Room ID", value=st.session_state.room_id, key="room_id_input", disabled=True)
    st.text_input("Your ID", value=st.session_state.user_id, key="user_id_input", disabled=True)
    st.info("Keep the Room ID unchanged when opening this page on another phone. The public Streamlit URL is what you share.")

    if st.button("Refresh page"):
        st.rerun()

html_code = """
<div style="max-width: 900px; margin: 0 auto; text-align: center;">
  <video id="cameraPreview" autoplay playsinline muted style="width: 100%; max-width: 760px; border-radius: 16px; background: #111; min-height: 420px;"></video>
  <div id="statusBox" style="margin-top: 12px; font-weight: 600; color: #0f766e;">Waiting for camera access...</div>
</div>
<script>
const video = document.getElementById('cameraPreview');
const statusBox = document.getElementById('statusBox');

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    video.srcObject = stream;
    statusBox.textContent = 'Camera is active. Open the Streamlit URL on another device to test the page.';
    statusBox.style.color = '#0f766e';
  } catch (error) {
    statusBox.textContent = 'Camera access was blocked. Please allow camera and microphone access in the browser.';
    statusBox.style.color = '#b91c1c';
  }
}

startCamera();
</script>
"""

st.components.v1.html(html_code, height=560)

st.success("The app is now served directly from the Streamlit URL. Open that URL on a phone or browser to view the camera preview.")

st.markdown("""
### What to do next
1. Open the public Streamlit URL in a browser or on your phone.
2. Allow camera and microphone access.
3. The preview should appear immediately.
""")

