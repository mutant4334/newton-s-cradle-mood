import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# File paths
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "eleven_moods.json"

# Mood mappings (number → label)
MOODS = {
    0: "😊 Happy", 1: "😢 Sad", 2: "😠 Angry", 3: "🤩 Excited", 4: "😰 Anxious",
    5: "😮 Surprised", 6: "🥱 Bored", 7: "😕 Confused", 8: "❤️ Loved",
    9: "🙏 Grateful", 10: "😌 Calm"
}

# Load Lottie file
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Initialize mood data file if it doesn't exist
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS}, f)

# Load mood data
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# Streamlit config
st.set_page_config(page_title="Mood Cradle", layout="centered")
st.title("💫 Newton's Cradle Mood Survey")

# Session state
if "animation_played" not in st.session_state:
    st.session_state.animation_played = False
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = None

# Show full animation only once
if not st.session_state.animation_played:
    st.markdown("🎬 Watch the animation before choosing your mood:")
    lottie = load_lottiefile(LOTTIE_FILE)
    st_lottie(lottie, speed=1, loop=False, height=300)
    st.session_state.animation_played = True
    st.stop()

# Mood selection after animation
if st.session_state.mood_selected is None:
    st.subheader("👇 Tap your current mood:")
    cols = st.columns(4)
    for i in MOODS:
        if cols[i % 4].button(MOODS[i]):
            mood_data[str(i)] += 1
            with open(MOOD_FILE, "w") as f:
                json.dump(mood_data, f)
            st.session_state.mood_selected = i
            st.success(f"✅ Mood '{MOODS[i]}' selected!")
            st.experimental_rerun()

# Show selected mood only
else:
    selected_mood = MOODS[st.session_state.mood_selected]
    st.subheader("🧘 You are feeling:")
    st.markdown(f"<h2 style='text-align:center'>{selected_mood}</h2>", unsafe_allow_html=True)

# Mood bar chart
st.subheader("📊 Mood Survey Results")
labels = [MOODS[int(k)] for k in mood_data]
counts = [mood_data[k] for k in mood_data]

fig, ax = plt.subplots()
ax.bar(labels, counts, color='skyblue')
ax.set_ylabel("Responses")
ax.set_title("Current Mood Distribution")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

st.caption("🔒 Anonymous · 🌐 Real-time · ✨ Built with Streamlit")
