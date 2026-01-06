import streamlit as st
from gtts import gTTS
import tempfile
import os
import math

st.set_page_config(page_title="Kids Touch Letters", layout="wide")

st.markdown(
    "<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch the Letter 🎈</h1>",
    unsafe_allow_html=True
)

# ---------------- SPEAK FUNCTION ----------------
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, autoplay=True)
        os.remove(fp.name)

# ---------------- RESPONSIVE GRID ----------------
def responsive_grid(items, columns, lang, prefix):
    cols = st.columns(columns)
    for i, item in enumerate(items):
        with cols[i % columns]:
            if st.button(item, use_container_width=True, key=f"{prefix}{i}"):
                speak(item, lang)

# Detect screen size approx
screen_width = st.session_state.get("screen_width", 1200)

# Adaptive columns
if screen_width < 600:
    col_count = 4
elif screen_width < 900:
    col_count = 6
else:
    col_count = 8

# ---------------- DATA (REAL ORDER) ----------------
english_letters = [chr(i) for i in range(65, 91)]  # A-Z

numbers = [str(i) for i in range(10)]  # 0-9

hindi_letters = [
    # स्वर
    "अ","आ","इ","ई","उ","ऊ","ऋ","ए","ऐ","ओ","औ",
    # व्यंजन
    "क","ख","ग","घ","ङ",
    "च","छ","ज","झ","ञ",
    "ट","ठ","ड","ढ","ण",
    "त","थ","द","ध","न",
    "प","फ","ब","भ","म",
    "य","र","ल","व",
    "श","ष","स","ह",
    "क्ष","त्र","ज्ञ"
]

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🔤 Alphabets", "🔢 Numbers", "🪔 Hindi Letters"])

with tab1:
    responsive_grid(english_letters, col_count, "en", "EN")

with tab2:
    responsive_grid(numbers, col_count, "en", "NUM")

with tab3:
    responsive_grid(hindi_letters, col_count, "hi", "HI")