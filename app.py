!pip install streamlit matplotlib
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
st.markdown("<h1 class='title'>🎯 Newton's Cradle Mood Survey (5 Moods)</h1>", unsafe_allow_html=True)
st.markdown("Choose your current **mood** below:")

# ---------- Custom Styling for Aesthetics ----------
st.markdown("""
    <style>
        /* Global Styles */
        body {
            background-color: #f5f5f5;
            font-family: 'Helvetica Neue', sans-serif;
            color: #333;
        }

        /* Title Styling */
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #3e4e57;
            text-align: center;
            margin-top: 40px;
            margin-bottom: 20px;
        }

        /* Subheader Styling */
        .subheader {
            font-size: 22px;
            font-weight: 600;
            color: #FF4081;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        /* Button Styling */
        .button {
            font-size: 18px;
            font-weight: bold;
            padding: 15px 25px;
            background-color: #FF4081;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.3s;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
        }

        .button:hover {
            background-color: #D81B60;
            transform: translateY(-5px);
        }

        .button:active {
            transform: translateY(0);
            background-color: #C2185B;
        }

        /* Container Layout for Buttons */
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            flex-wrap: wrap;
            gap: 20px;
        }

        /* Mood Option Styling */
        .mood-btn {
            width: 180px;
            height: 100px;
            border-radius: 12px;
            font-size: 20px;
            font-weight: bold;
            background-color: #F48FB1;
            color: white;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        }

        .mood-btn:hover {
            background-color: #F06292;
            transform: scale(1.05);
        }

        /* Chart Styling */
        .piechart {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
        }

        /* Password Box Styling */
        .password-box {
            width: 300px;
            padding: 12px;
            margin-top: 20px;
            border: 1px solid #FF4081;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 16px;
        }

        /* Footer Styling */
        footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Password protection
password = st.text_input("Enter Password", type="password", key="password_input")
if password == PASSWORD:
    st.success("Access granted!")

    # Display mood options
    st.markdown("<h2 class='subheader'>Select Your Mood</h2>", unsafe_allow_html=True)

    # Layout for mood buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        for i in range(0, 2):
            if st.button(MOODS[i], key=i):
                mood_data[str(i)] += 1
    with col2:
        for i in range(2, 4):
            if st.button(MOODS[i], key=i):
                mood_data[str(i)] += 1
    with col3:
        if st.button(MOODS[4], key=4):
            mood_data[str(4)] += 1

    # Save updated mood data
    with open(MOOD_FILE, "w") as f:
        json.dump(mood_data, f)

    # Show mood pie chart
    st.markdown("<div class='piechart'>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(list(mood_data.values()), labels=MOODS.values(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Incorrect password, please try again.")
