import streamlit as st
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Kids Learning App", layout="wide")

st.title("🎈 Learn Letters & Numbers 🎈")
st.write("👉 Touch a letter or number to hear its sound!")

# Function to play sound
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name)
        os.remove(fp.name)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔤 Alphabets", "🔢 Numbers", "🪔 Hindi Letters"])

# ---------------- ENGLISH ALPHABETS ----------------
with tab1:
    letters = [chr(i) for i in range(65, 91)]
    cols = st.columns(6)
    for i, letter in enumerate(letters):
        if cols[i % 6].button(letter, use_container_width=True):
            speak(letter, "en")

# ---------------- NUMBERS ----------------
with tab2:
    numbers = [str(i) for i in range(10)]
    cols = st.columns(5)
    for i, num in enumerate(numbers):
        if cols[i % 5].button(num, use_container_width=True):
            speak(num, "en")

# ---------------- HINDI LETTERS ----------------
with tab3:
    hindi_letters = [
        "अ","आ","इ","ई","उ","ऊ","ए","ऐ","ओ","औ",
        "क","ख","ग","घ","च","छ","ज","झ",
        "ट","ठ","ड","ढ","त","थ","द","ध",
        "न","प","फ","ब","भ","म","य","र",
        "ल","व","श","ष","स","ह"
    ]

    cols = st.columns(6)
    for i, letter in enumerate(hindi_letters):
        if cols[i % 6].button(letter, use_container_width=True):
            speak(letter, "hi")