import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# File paths
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "eleven_moods.json"

# Map mood numbers to labels
MOODS = {
    0: "😊 Happy", 1: "😢 Sad", 2: "😠 Angry", 3: "🤩 Excited", 4: "😰 Anxious",
    5: "😮 Surprised", 6: "🥱 Bored", 7: "😕 Confused", 8: "❤️ Loved",
    9: "🙏 Grateful", 10: "😌 Calm"
}

# Owner password to view results
OWNER_PASSWORD = "whey@protein"

# Load Lottie animation
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Initialize data file if not exists
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS.keys()}, f)

# Load mood data
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# Config
st.set_page_config(page_title="Mood Cradle", layout="centered")
st.title("🧠 How are you feeling today")

# Show Lottie animation if mood not yet selected
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = None

if st.session_state.mood_selected is None:
    lottie_animation = load_lottiefile(LOTTIE_FILE)
    st_lottie(lottie_animation, speed=1, loop=True, height=250)

st.markdown("Tap your current **mood** and contribute anonymously 🌐")

# Show mood buttons
st.subheader("👇 Select a mood:")
cols = st.columns(4)

for i in MOODS:
    if cols[i % 4].button(MOODS[i]):
        mood_data[str(i)] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.session_state.mood_selected = i
        st.success(f"✅ Mood '{MOODS[i]}' selected!")
        break

# If mood selected, show confirmation
if st.session_state.mood_selected is not None:
    st.markdown(f"🧘‍♂️ You feel: **{MOODS[st.session_state.mood_selected]}**")

# Password prompt for owner to view results
password = st.text_input("Enter admin password to view results:", type="password")

if password == OWNER_PASSWORD:
    st.subheader("📊 Mood Survey Results (Admin Only)")
    labels = [MOODS[int(k)] for k in mood_data.keys()]
    counts = [mood_data[k] for k in mood_data.keys()]

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color='coral')
    ax.set_ylabel("Responses")
    ax.set_title("Mood Distribution")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    st.caption("🧪 Built with Streamlit | 🔒 Protected by Admin Password")
elif password != "" and password != OWNER_PASSWORD:
    st.warning("🚫 Incorrect password. You are not authorized to view results.")
