import streamlit as st
from gtts import gTTS
import tempfile
import base64
import os

st.set_page_config(page_title="Kids Touch Letters", layout="wide")

st.markdown(
    "<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch the Letter 🎈</h1>",
    unsafe_allow_html=True
)

# ---------------- PLAY SOUND (NO PLAYER) ----------------
def play_sound(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio_bytes = open(f.name, "rb").read()
        encoded = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{encoded}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove(f.name)

# ---------------- RESPONSIVE GRID ----------------
def grid(items, cols, lang, key_prefix):
    columns = st.columns(cols)
    for i, item in enumerate(items):
        with columns[i % cols]:
            if st.button(item, use_container_width=True, key=f"{key_prefix}{i}"):
                play_sound(item, lang)

# ---------------- COLUMN COUNT ----------------
width = st.session_state.get("width", 1200)
if width < 600:
    COLS = 4
elif width < 900:
    COLS = 6
else:
    COLS = 8

# ---------------- DATA (REAL ORDER) ----------------
english = [chr(i) for i in range(65, 91)]

numbers = [str(i) for i in range(10)]

hindi = [
    "अ","आ","इ","ई","उ","ऊ","ऋ","ए","ऐ","ओ","औ",
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
    grid(english, COLS, "en", "EN")

with tab2:
    grid(numbers, COLS, "en", "NUM")

with tab3:
    grid(hindi, COLS, "hi", "HI")