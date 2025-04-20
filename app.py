
import streamlit as st
from gtts import gTTS
import os

st.title("AI Voice Maker")

text_input = st.text_area("Nhập văn bản tiếng Anh để chuyển thành giọng nói")

if st.button("Tạo giọng nói"):
    if text_input.strip() != "":
        tts = gTTS(text_input)
        tts.save("output.mp3")
        audio_file = open("output.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        st.success("Đã tạo giọng nói thành công!")
    else:
        st.warning("Vui lòng nhập văn bản trước khi tạo giọng nói.")
