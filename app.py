import streamlit as st
import json
import os
import matplotlib.pyplot as plt

# ---------- Configuration ----------
MOOD_FILE = "moods_data.json"
PASSWORD = "owner123"  # Change this to your own password

MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "🤩 Excited",
    4: "😌 Calm"
}

# ---------- Initialize mood data file ----------
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS}, f)

# ---------- Load mood data ----------
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# ---------- Streamlit Page Setup ----------
st.set_page_config(page_title="Mood Cradle Survey", layout="centered")
st.title("🎯 Newton's Cradle Mood Survey (5 Moods)")
st.markdown("Choose your current **mood** below:")

# ---------- Mood Selection ----------
st.subheader("👇 Tap a mood:")
cols = st.columns(5)

for i in MOODS:
    if cols[i % 5].button(MOODS[i]):
        mood_data[str(i)] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.success(f"✅ Mood '{MOODS[i]}' recorded!")
        st.stop()

# ---------- Owner-only Result Access ----------
st.markdown("---")
st.subheader("🔐 View Mood Results (Owner Only)")
password = st.text_input("Enter password to view results:", type="password")

if password == PASSWORD:
    st.success("Access granted. Showing results...")

    # Plot pie chart
    labels = [MOODS[int(k)] for k in mood_data]
    sizes = [mood_data[k] for k in mood_data]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, startangle=90, autopct='%1.1f%%', shadow=True)
    ax.axis('equal')
    st.pyplot(fig)

    # Reset option
    if st.button("♻️ Reset All Results"):
        with open(MOOD_FILE, "w") as f:
            json.dump({str(k): 0 for k in MOODS}, f)
        st.success("✅ All results reset.")
        st.experimental_rerun()
elif password:
    st.error("Incorrect password.")

# ---------- Footer ----------
st.caption("📊 Anonymous & Secure | Built with ❤️ using Streamlit")
