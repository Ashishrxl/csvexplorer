import streamlit as st
from gtts import gTTS
import tempfile
import base64
import os
import random

st.set_page_config(page_title="Kids Touch Letters", layout="wide")

# ---------- CSS FOR COLORFUL BUTTONS ----------
st.markdown("""
<style>
button {
    font-size: 36px !important;
    font-weight: 900 !important;
    height: 90px !important;
    border-radius: 20px !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch the Letter 🎈</h1>",
    unsafe_allow_html=True
)

# ---------- PLAY SOUND (HIDDEN PLAYER) ----------
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

# ---------- RESPONSIVE COLUMN COUNT ----------
def get_columns():
    width = st.session_state.get("width", 1200)
    if width < 500:
        return 3      # small mobile
    elif width < 800:
        return 4      # large mobile / small tablet
    elif width < 1100:
        return 6      # tablet
    else:
        return 8      # desktop

# ---------- COLOR PALETTE ----------
colors = [
    "#ff6f61", "#f7b731", "#20bf6b", "#45aaf2",
    "#a55eea", "#fd9644", "#2d98da", "#eb3b5a"
]

# ---------- GRID (ORDER PRESERVED) ----------
def letter_grid(items, lang, key_prefix):
    cols_count = get_columns()
    rows = [items[i:i+cols_count] for i in range(0, len(items), cols_count)]

    for r, row in enumerate(rows):
        cols = st.columns(cols_count)
        for c, letter in enumerate(row):
            color = random.choice(colors)
            cols[c].markdown(
                f"""
                <style>
                div[data-testid="stButton"] > button {{
                    background-color: {color};
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            if cols[c].button(letter, use_container_width=True, key=f"{key_prefix}{r}{c}"):
                play_sound(letter, lang)

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
    letter_grid(english_letters, "en", "EN")

with tab2:
    letter_grid(numbers, "en", "NUM")

with tab3:
    letter_grid(hindi_letters, "hi", "HI")