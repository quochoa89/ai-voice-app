import streamlit as st
from utils import generate_video_from_script
import tempfile
import os

st.set_page_config(page_title="Script to Video", layout="centered")

st.title("📽️ Convert Script to Video")

# --- Upload background image ---
bg_image = st.file_uploader("🖼️ Upload background image", type=["jpg", "jpeg", "png"])

# --- Script input ---
script = st.text_area("📝 Enter your script", height=250)

# --- Options ---
col1, col2, col3 = st.columns(3)
with col1:
    show_subtitle = st.checkbox("🧾 Show subtitles", value=True)
with col2:
    layout = st.selectbox("📐 Video layout", ["16:9", "9:16"])
with col3:
    max_chars = st.slider("✂️ Split every (chars)", 100, 500, 300, step=50)

# --- Generate Button ---
if st.button("🎬 Generate Video") and script and bg_image:
    with st.spinner("Generating video..."):
        temp_video = generate_video_from_script(script, bg_image, show_subtitle, layout, max_chars)
        st.success("✅ Video generated!")
        st.video(temp_video)
        with open(temp_video, "rb") as f:
            st.download_button("⬇️ Download Video", f, file_name="output.mp4", mime="video/mp4")
