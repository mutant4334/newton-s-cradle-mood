import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# File paths
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "eleven_moods.json"  # Ensure this is the correct path to your Lottie animation file

# Mood mappings (number → label)
MOODS = {
    0: "😊 Happy", 1: "😢 Sad", 2: "😠 Angry", 3: "🤩 Excited", 4: "😰 Anxious",
    5: "😮 Surprised", 6: "🥱 Bored", 7: "😕 Confused", 8: "❤️ Loved",
    9: "🙏 Grateful", 10: "😌 Calm"
}

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

# Function to load the Lottie file
def load_lottiefile(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lottie file not found at {filepath}. Please check the file path.")
        return None

# Display animation first
if not st.session_state.animation_played:
    st.markdown("🎬 Watch the animation before choosing your mood:")
    
    # Load and display the Lottie animation
    lottie = load_lottiefile(LOTTIE_FILE)
    
    if lottie:
        st_lottie(lottie, speed=1, loop=False, height=300)
        # Mark animation as played in session state after animation is shown
        st.session_state.animation_played = True

else:
    # After animation, display mood selection buttons
    if st.session_state.mood_selected is None:
        st.subheader("👇 Tap your current mood:")
        cols = st.columns(4)  # Display buttons in 4 columns
        for i in MOODS:
            if cols[i % 4].button(MOODS[i]):
                mood_data[str(i)] += 1
                with open(MOOD_FILE, "w") as f:
                    json.dump(mood_data, f)
                st.session_state.mood_selected = i  # Save the selected mood
                st.success(f"✅ Mood '{MOODS[i]}' selected!")

    # After selecting a mood, show the mood
    if st.session_state.mood_selected is not None:
        selected_mood = MOODS[st.session_state.mood_selected]
        st.subheader("🧘 You are feeling:")
        st.markdown(f"<h2 style='text-align:center'>{selected_mood}</h2>", unsafe_allow_html=True)

    # Show the mood distribution bar chart
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
