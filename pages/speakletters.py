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

# ---------- SOUND (NO PLAYER) ----------
def play_sound(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio = open(f.name, "rb").read()
    encoded = base64.b64encode(audio).decode()
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{encoded}">
        </audio>
        """,
        unsafe_allow_html=True
    )
    os.remove(f.name)

# ---------- GRID THAT PRESERVES ORDER ----------
def ordered_grid(items, columns, lang, prefix):
    rows = [items[i:i+columns] for i in range(0, len(items), columns)]
    for r, row in enumerate(rows):
        cols = st.columns(columns)
        for c, item in enumerate(row):
            if cols[c].button(item, use_container_width=True, key=f"{prefix}{r}{c}"):
                play_sound(item, lang)

# ---------- RESPONSIVE COLUMN COUNT ----------
width = st.session_state.get("width", 1200)
if width < 600:
    COLS = 4
elif width < 900:
    COLS = 6
else:
    COLS = 8

# ---------- DATA (FIXED ORDER) ----------
english_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

numbers = list("0123456789")

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
    "श","ष","स","ह"
]

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["🔤 Alphabets", "🔢 Numbers", "🪔 Hindi Letters"])

with tab1:
    ordered_grid(english_letters, COLS, "en", "EN")

with tab2:
    ordered_grid(numbers, COLS, "en", "NUM")

with tab3:
    ordered_grid(hindi_letters, COLS, "hi", "HI")