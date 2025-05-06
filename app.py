import streamlit as st
import json
import os
import plotly.express as px

# --- CONFIG ---
MOOD_FILE = "moods_data.json"
OWNER_PASSWORD = "admin123"  # 🔒 Change this to your private password

MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "🤩 Excited",
    4: "😌 Calm"
}

# --- INIT ---
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS.keys()}, f)

with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Mood Pie", layout="centered")
st.title("🎯 Mood Pie Survey")

st.markdown("Tap the mood you're feeling right now. It's anonymous and helps track the vibe! 🌐")

# --- PIE CHART ---
labels = [MOODS[int(k)] for k in mood_data.keys()]
values = [mood_data[k] for k in mood_data.keys()]
colors = px.colors.qualitative.Pastel

fig = px.pie(
    names=labels,
    values=values,
    title="Live Mood Distribution",
    color_discrete_sequence=colors,
    hole=0.3
)
fig.update_traces(textinfo='label+percent', pull=[0.05]*len(labels))

st.plotly_chart(fig, use_container_width=True)

# --- MOOD SELECTION ---
st.subheader("👇 How do you feel?")
cols = st.columns(5)

for i in MOODS:
    if cols[i % 5].button(MOODS[i]):
        mood_data[str(i)] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.success(f"✅ You selected: {MOODS[i]}")
        st.rerun()

# --- OWNER TOOLS ---
st.markdown("---")
with st.expander("🔒 Admin Panel"):
    password = st.text_input("Enter admin password to view or reset data:", type="password")

    if password == OWNER_PASSWORD:
        st.success("🔐 Access granted!")

        if st.button("🔄 Reset All Data"):
            mood_data = {str(k): 0 for k in MOODS}
            with open(MOOD_FILE, "w") as f:
                json.dump(mood_data, f)
            st.success("✅ Mood data has been reset!")
            st.rerun()

        st.subheader("📊 Current Mood Data")
        st.json(mood_data)
    elif password:
        st.error("❌ Incorrect password!")

st.caption("✨ Made with Streamlit | Anonymous & Real-time")
