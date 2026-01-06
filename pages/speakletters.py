import streamlit as st
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Kids Touch & Learn", layout="wide")

st.markdown(
    "<h1 style='text-align:center;color:#ff6f61;'>🎈 Touch & Learn 🎈</h1>",
    unsafe_allow_html=True
)

# Speak function
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, autoplay=True)
        os.remove(fp.name)

# ---------------- DATA ----------------
alphabets = [
    ("A", "Apple"), ("B", "Ball"), ("C", "Cat"), ("D", "Dog"), ("E", "Elephant"),
    ("F", "Fish"), ("G", "Grapes"), ("H", "Hen"), ("I", "Ice Cream"), ("J", "Jug"),
    ("K", "Kite"), ("L", "Lion"), ("M", "Mango"), ("N", "Nest"), ("O", "Orange"),
    ("P", "Parrot"), ("Q", "Queen"), ("R", "Rabbit"), ("S", "Sun"), ("T", "Tiger"),
    ("U", "Umbrella"), ("V", "Van"), ("W", "Watch"), ("X", "Xylophone"),
    ("Y", "Yak"), ("Z", "Zebra")
]

numbers = [
    ("0", "Zero"), ("1", "One"), ("2", "Two"), ("3", "Three"), ("4", "Four"),
    ("5", "Five"), ("6", "Six"), ("7", "Seven"), ("8", "Eight"), ("9", "Nine")
]

hindi_swar = [
    ("अ", "अनार"), ("आ", "आम"), ("इ", "इमली"), ("ई", "ईख"),
    ("उ", "उल्लू"), ("ऊ", "ऊन"), ("ए", "एड़ी"), ("ऐ", "ऐनक"),
    ("ओ", "ओखली"), ("औ", "औरत")
]

hindi_vyanjan = [
    ("क", "कमल"), ("ख", "खरगोश"), ("ग", "गाय"), ("घ", "घर"),
    ("च", "चम्मच"), ("छ", "छाता"), ("ज", "जहाज"), ("झ", "झंडा"),
    ("ट", "टमाटर"), ("ठ", "ठेला"), ("ड", "डमरू"), ("ढ", "ढोल"),
    ("त", "तरबूज"), ("थ", "थाली"), ("द", "दवात"), ("ध", "धनुष"),
    ("न", "नल"), ("प", "पतंग"), ("फ", "फल"), ("ब", "बतख"),
    ("भ", "भालू"), ("म", "मछली"), ("य", "योग"), ("र", "रथ"),
    ("ल", "लड्डू"), ("व", "वन"), ("श", "शेर"), ("ष", "षट्कोण"),
    ("स", "सूरज"), ("ह", "हाथी")
]

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🔤 Alphabets", "🔢 Numbers", "🪔 Hindi Letters"])

# ---------------- ALPHABETS ----------------
with tab1:
    cols = st.columns(5)
    for i, (letter, word) in enumerate(alphabets):
        with cols[i % 5]:
            st.image(f"https://via.placeholder.com/150?text={word}", width=150)
            if st.button(f"{letter} - {word}", key=f"A{i}"):
                speak(f"{letter} for {word}", "en")

# ---------------- NUMBERS ----------------
with tab2:
    cols = st.columns(5)
    for i, (num, word) in enumerate(numbers):
        with cols[i % 5]:
            st.image(f"https://via.placeholder.com/150?text={word}", width=150)
            if st.button(f"{num} - {word}", key=f"N{i}"):
                speak(f"{num}", "en")

# ---------------- HINDI ----------------
with tab3:
    st.subheader("🔸 स्वर")
    cols = st.columns(5)
    for i, (letter, word) in enumerate(hindi_swar):
        with cols[i % 5]:
            st.image(f"https://via.placeholder.com/150?text={word}", width=150)
            if st.button(f"{letter} - {word}", key=f"S{i}"):
                speak(f"{letter} {word}", "hi")

    st.subheader("🔸 व्यंजन")
    cols = st.columns(5)
    for i, (letter, word) in enumerate(hindi_vyanjan):
        with cols[i % 5]:
            st.image(f"https://via.placeholder.com/150?text={word}", width=150)
            if st.button(f"{letter} - {word}", key=f"V{i}"):
                speak(f"{letter} {word}", "hi")