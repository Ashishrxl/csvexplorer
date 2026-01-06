import streamlit as st
from gtts import gTTS
import tempfile
import base64
import os

st.set_page_config(page_title="Kids Touch Letters", layout="wide")

st.markdown("""
<style>
button {
    font-size: 36px !important;
    font-weight: 900 !important;
    height: 90px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch the Letter 🎈</h1>",
    unsafe_allow_html=True
)

# ---------- PLAY SOUND (NO PLAYER) ----------
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

# ---------- RESPONSIVE GRID ----------
def ordered_grid(items, lang, prefix):
    screen_width = st.session_state.get("width", 1200)
    if screen_width < 600:
        cols_count = 4
    elif screen_width < 900:
        cols_count = 6
    else:
        cols_count = 8

    rows = [items[i:i+cols_count] for i in range(0, len(items), cols_count)]

    for r, row in enumerate(rows):
        cols = st.columns(cols_count)
        for c, item in enumerate(row):
            if cols[c].button(item, use_container_width=True, key=f"{prefix}{r}{c}"):
                play_sound(item, lang)

# ---------- DATA (CORRECT ORDER) ----------
english_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

numbers = list("0123456789")

hindi_letters = [
    "अ","आ","इ","ई","उ","ऊ","ऋ","ए","ऐ","ओ","औ",
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
    ordered_grid(english_letters, "en", "EN")

with tab2:
    ordered_grid(numbers, "en", "NUM")

with tab3:
    ordered_grid(hindi_letters, "hi", "HI")