from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import tempfile
import os
import textwrap
import uuid

def split_script(script, max_chars=300):
    # Tách đoạn dài thành các phần nhỏ
    paragraphs = script.split("\n")
    chunks = []
    for para in paragraphs:
        wrapped = textwrap.wrap(para, max_chars)
        chunks.extend(wrapped)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def generate_video_from_script(script, bg_image_file, show_subtitle, layout, max_chars):
    clips = []
    text_chunks = split_script(script, max_chars)

    # Xử lý ảnh nền
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp:
        img_tmp.write(bg_image_file.read())
        bg_path = img_tmp.name

    for idx, chunk in enumerate(text_chunks):
        # Tạo file audio từ text
        tts = gTTS(chunk)
        audio_path = f"/tmp/audio_{uuid.uuid4()}.mp3"
        tts.save(audio_path)

        # Load ảnh nền và resize đúng tỉ lệ
        img = Image.open(bg_path).convert("RGB")
        aspect = (1280, 720) if layout == "16:9" else (720, 1280)
        img = img.resize(aspect)
        img_path = f"/tmp/bg_{uuid.uuid4()}.png"
        img.save(img_path)

        # Tạo clip ảnh
        duration = AudioFileClip(audio_path).duration
        img_clip = ImageClip(img_path).set_duration(duration)

        # Thêm phụ đề nếu có chọn
        if show_subtitle:
            txt_clip = TextClip(chunk, fontsize=40, color='white', font="Arial-Bold",
                                size=(aspect[0]*0.9, None), method='caption')
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration)
            final_clip = CompositeVideoClip([img_clip, txt_clip])
        else:
            final_clip = img_clip

        # Gắn audio vào clip
        final_clip = final_clip.set_audio(AudioFileClip(audio_path))
        clips.append(final_clip)

    # Ghép tất cả thành một video
    final_video = concatenate_videoclips(clips, method="compose")

    # Lưu video tạm
    final_path = f"/tmp/final_{uuid.uuid4()}.mp4"
    final_video.write_videofile(final_path, codec='libx264', audio_codec='aac', fps=24, verbose=False, logger=None)

    return final_path
    from moviepy.editor import TextClip, CompositeVideoClip

def generate_video_from_script(script_text, output_path="output_video.mp4"):
    text_clip = TextClip(script_text, fontsize=24, color='white', size=(720, 480))
    text_clip = text_clip.set_duration(10)
    final_clip = CompositeVideoClip([text_clip])
    final_clip.write_videofile(output_path, fps=24)

