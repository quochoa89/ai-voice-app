import streamlit as st
from utils import generate_video_from_script
import os

st.title("Text to Video Generator")

text_input = st.text_area("Nhập văn bản để tạo video")

if st.button("Tạo Video"):
    if text_input.strip() != "":
        try:
            generate_video_from_script(text_input)
            st.video("output_video.mp4")
            st.success("Tạo video thành công!")
        except Exception as e:
            st.error(f"Lỗi khi tạo video: {e}")
    else:
        st.warning("Vui lòng nhập nội dung trước khi tạo video.")
