import streamlit as st
import json
import os
import matplotlib.pyplot as plt

from streamlit_lottie import st_lottie
import plotly.graph_objects as go

# Config
st.set_page_config(page_title="Mood Cradle", layout="centered")
st.title("🎯 Newton's Cradle Mood Survey")

# Constants
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "five_moods.json"  # Make sure you use correct 5-mood Lottie file
OWNER_PASSWORD = "your_password_here"

# Five mood options
MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "😰 Anxious",
    4: "😌 Calm"
}

# Functions
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def initialize_data_file():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump({str(k): 0 for k in MOODS.keys()}, f)

def save_data(data):
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

# Initialization
initialize_data_file()
mood_data = load_data()

# Session state
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = None

if "owner_access" not in st.session_state:
    st.session_state.owner_access = False

# Lottie Animation (Optional)
lottie_animation = load_lottiefile(LOTTIE_FILE)
st_lottie(lottie_animation, speed=1, loop=False, height=250)

# Mood Selection
st.markdown("### Tap to select your current **mood**:")

cols = st.columns(5)
for i in MOODS:
    if cols[i % 5].button(MOODS[i]):
        mood_data[str(i)] += 1
        save_data(mood_data)
        st.session_state.mood_selected = i
        st.success(f"✅ Mood '{MOODS[i]}' submitted anonymously!")
        break

# Show selected mood
if st.session_state.mood_selected is not None:
    st.markdown(f"🧘‍♂️ You feel: **{MOODS[st.session_state.mood_selected]}**")

# Owner login
with st.expander("🔒 Admin: View Results / Reset"):
    password_input = st.text_input("Enter password:", type="password")
    if st.button("Login as Owner"):
        if password_input == OWNER_PASSWORD:
            st.session_state.owner_access = True
            st.success("🟢 Access granted!")
        else:
            st.error("❌ Incorrect password.")

# Show results (owner only)
if st.session_state.owner_access:
    st.subheader("📊 Mood Survey Results")

    # Filter valid moods only
    labels = [MOODS[int(k)] for k in mood_data.keys() if int(k) in MOODS]
    values = [mood_data[k] for k in mood_data.keys() if int(k) in MOODS]

    # Plotly Pie Chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_traces(textinfo='label+percent', pull=[0.05]*len(labels), marker=dict(colors=['#FF9999','#66B2FF','#99FF99','#FFCC99','#CCCCFF']))
    st.plotly_chart(fig)

    # Reset button
    if st.button("🔄 Reset Mood Data"):
        save_data({str(k): 0 for k in MOODS.keys()})
        st.success("Data has been reset.")

st.caption("🧪 Built with Streamlit | 🔒 Anonymous & Real-time")
