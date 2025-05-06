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

# ---------- Custom Styling for Aesthetics ----------
st.markdown("""
    <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #4C8BF5;
        }
        .subheader {
            font-size: 20px;
            font-weight: 600;
            color: #F06292;
        }
        .button {
            font-size: 18px;
            padding: 15px;
            background-color: #FF4081;
            color: white;
            border: none;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #D81B60;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
        .piechart {
            border-radius: 10px;
            padding: 10px;
            background-color: #f1f1f1;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Mood Selection ----------
st.subheader("👇 Tap a mood:")
cols = st.columns(5)

# Buttons with Icons (Hover Effects)
for i in MOODS:
    if cols[i % 5].button(f"{MOODS[i]}", key=f"mood_{i}", help="Click to select mood", use_container_width=True):
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

    # ---------- Pie Chart Visualization ----------
    labels = [MOODS[int(k)] for k in mood_data]
    sizes = [mood_data[k] for k in mood_data]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, startangle=90, autopct='%1.1f%%', shadow=True)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    st.pyplot(fig)

    # ---------- Reset Option for the Owner ----------
    if st.button("♻️ Reset All Results"):
        with open(MOOD_FILE, "w") as f:
            json.dump({str(k): 0 for k in MOODS}, f)
        st.success("✅ All results reset.")
        st.experimental_rerun()

elif password:
    st.error("Incorrect password.")

# ---------- Footer ----------
st.caption("📊 Anonymous & Secure | Built with ❤️ using Streamlit")
