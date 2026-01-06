import streamlit as st
from gtts import gTTS
import tempfile
from num2words import num2words
import random
import os
import base64

st.set_page_config(page_title="Kids Touch Letters", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
button {
    font-size: 36px !important;
    font-weight: 900 !important;
    height: 90px !important;
    border-radius: 20px !important;
    color: white !important;
}

/* Hide default audio player */
.audio-container audio {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch the Letter 🎈</h1>", unsafe_allow_html=True)

# ---------- PLAY SOUND ----------
def play_sound(text, lang):
    """Generate TTS and play, hiding the player"""
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio_path = f.name

    # Read audio as base64 and embed in hidden player
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    rand = random.randint(1, 1_000_000)
    st.markdown(
        f"""
        <div class="audio-container">
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}?v={rand}" type="audio/mp3">
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Remove temp file
    os.remove(audio_path)

# ---------- PLAY ALL ----------
def play_all_sounds(items, lang, number_words=False):
    if number_words:
        text_items = [num2words(int(i)) for i in items]
    else:
        text_items = items
    text = " ".join(text_items)
    play_sound(text, lang)

# ---------- GRID ----------
def get_columns():
    width = st.session_state.get("width", 1200)
    if width < 500: return 3
    elif width < 800: return 4
    elif width < 1100: return 6
    else: return 8

colors = ["#ff6f61","#f7b731","#20bf6b","#45aaf2","#a55eea","#fd9644","#2d98da","#eb3b5a"]

def letter_grid(items, lang, key_prefix, number_words=False):
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
            if cols[c].button(letter, use_container_width=True, key=f"{key_prefix}_{r}_{c}_{random.randint(0,1_000_000)}"):
                spoken = num2words(int(letter)) if number_words else letter
                play_sound(spoken, lang)

# ---------- DATA ----------
english_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = [str(i) for i in range(0, 21)]
hindi_letters = [
    "अ","आ","इ","ई","उ","ऊ","ऋ","ए","ऐ","ओ","औ",
    "क","ख","ग","घ","ङ","च","छ","ज","झ","ञ",
    "ट","ठ","ड","ढ","ण","त","थ","द","ध","न",
    "प","फ","ब","भ","म","य","र","ल","व",
    "श","ष","स","ह","क्ष","त्र","ज्ञ"
]

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["🔤 Alphabets", "🔢 Numbers", "🪔 Hindi Letters"])

with tab1:
    st.markdown("### 🔊 Listen to All Alphabets")
    if st.button("▶️ Play All Alphabets", use_container_width=True):
        play_all_sounds(english_letters, "en")
    letter_grid(english_letters, "en", "EN")

with tab2:
    st.markdown("### 🔊 Listen to All Numbers")
    if st.button("▶️ Play All Numbers", use_container_width=True):
        play_all_sounds(numbers, "en", number_words=True)
    letter_grid(numbers, "en", "NUM", number_words=True)

with tab3:
    st.markdown("### 🔊 Listen to All Hindi Letters")
    if st.button("▶️ Play All Hindi Letters", use_container_width=True):
        play_all_sounds(hindi_letters, "hi")
    letter_grid(hindi_letters, "hi", "HI")