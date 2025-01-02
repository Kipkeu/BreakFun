import streamlit as st
import random
import json
from datetime import datetime, timedelta

# Load activities from file
def load_activities():
    with open("activities.json", "r") as file:
        return json.load(file)

# Load or initialize user data for all users
def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)

# Get the top 3 users
def get_top_users(user_data):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    return sorted_users[:3]

# Streamlit App
st.title("Fun Activity Platform 🎉")

# Load data
user_data = load_user_data()
activities = load_activities()
today = datetime.now().date()

# Section: User Login/Signup
st.subheader("Step 1: Login or Signup")
username = st.text_input("Enter your username:")
if username:
    if username not in user_data:
        user_data[username] = {"points": 0, "last_activity_date": None, "last_image_uploaded": None}
        st.success(f"Welcome, {username}! Your account has been created.")
    else:
        st.success(f"Welcome back, {username}!")

    # Proceed only if username is valid
    user = user_data[username]

    # Section: Get Today's Activity
    st.subheader("Step 2: Get Your Daily Activity")
    if user.get("last_activity_date") != str(today):
        st.write("Click the button to get today's activity!")
        if st.button("Get Activity"):
            activity = random.choice(activities)

            user["last_activity_date"] = str(today)
            save_user_data(user_data)

            st.write(f"**Today's activity:** {activity}")
            if st.button("Mark as Done"):
                user["points"] += 10
                save_user_data(user_data)
                st.success(f"You've earned 10 points! Total points: {user['points']}")
    else:
        st.info("You already completed today's activity!")
        st.write(f"Total points: {user['points']}")

    # Section: Upload an Activity Picture
    st.subheader("Step 3: Upload Your Activity Picture")
    uploaded_file = st.file_uploader("Upload a picture of your activity (jpg, png, jpeg):", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        if user.get("last_image_uploaded") != str(today):
            user["points"] += 5  # Extra points for uploading an image
            user["last_image_uploaded"] = str(today)
            save_user_data(user_data)
            st.success("Picture uploaded successfully! You've earned 5 extra points.")
        else:
            st.info("You already uploaded a picture for today.")
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        st.write(f"Total points: {user['points']}")

    # Section: Weekly Leaderboard
    st.subheader("Top Users This Week")
    top_users = get_top_users(user_data)
    if top_users:
        for i, (name, data) in enumerate(top_users, start=1):
            st.write(f"**{i}. {name}** - {data['points']} points")
    else:
        st.write("No users yet!")
