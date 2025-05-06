import streamlit as st
import json
import os
import plotly.express as px
from streamlit_lottie import st_lottie

# Constants
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "eleven_moods.json"
OWNER_PASSWORD = "admin@123"  # 🔐 Change this to your preferred password

# Only 5 moods
MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "🤩 Excited",
    4: "😌 Calm"
}

# Load Lottie animation
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Init mood file
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS.keys()}, f)

# Load mood data
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# App config
st.set_page_config(page_title="Mood Cradle", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🧠 Newton's Cradle Mood Survey</h1>", unsafe_allow_html=True)

# Animation
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = None

if st.session_state.mood_selected is None:
    if os.path.exists(LOTTIE_FILE):
        lottie_animation = load_lottiefile(LOTTIE_FILE)
        st_lottie(lottie_animation, speed=1, loop=True, height=250)

st.markdown("<h4 style='text-align: center;'>💬 Tap your current <i>mood</i> and contribute anonymously 🌐</h4>", unsafe_allow_html=True)

# Mood Buttons
st.subheader("👇 Select a mood:")
cols = st.columns(5)
for i in MOODS:
    if cols[i % 5].button(MOODS[i]):
        mood_data[str(i)] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.session_state.mood_selected = i
        st.success(f"✅ Mood '{MOODS[i]}' selected!")
        break

# Show selected mood
if st.session_state.mood_selected is not None:
    st.markdown(f"<h5 style='text-align:center;'>🧘‍♂️ You feel: <b>{MOODS[st.session_state.mood_selected]}</b></h5>", unsafe_allow_html=True)

# Admin Section
st.divider()
st.subheader("🔐 Admin Access (for Results & Reset)")
password = st.text_input("Enter password to view results:", type="password")

if password == OWNER_PASSWORD:
    show_results = True
    st.success("🔓 Access granted!")
else:
    show_results = False
    if password:
        st.error("❌ Incorrect password.")

# Pie Chart
if show_results:
    st.subheader("📊 Mood Survey Results")

    labels = [MOODS[int(k)] for k in mood_data.keys()]
    counts = [mood_data[k] for k in mood_data.keys()]
    pie_data = {"Mood": labels, "Count": counts}

    fig = px.pie(
        pie_data, names="Mood", values="Count",
        title="Mood Distribution", hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textinfo="label+percent", pull=[0.05] * len(labels))
    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔄 Reset Mood Data (Owner Only)"):
        mood_data = {str(k): 0 for k in MOODS.keys()}
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.success("✅ Mood data has been reset.")

st.caption("🧪 Built with Streamlit | 🔒 Anonymous & Real-time | 🎨 Styled with Plotly")
