import streamlit as st
import random
import json
from datetime import datetime

# Load activities from file
def load_activities():
    with open("activities.json", "r") as file:
        return json.load(file)

# Load or initialize user data
def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"points": 0, "last_activity_date": None}

def save_user_data(data):
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)

# Streamlit App
st.title("Fun Activity Platform 🎉")

# Load user data and today's date
user_data = load_user_data()
today = datetime.now().date()

if user_data.get("last_activity_date") != str(today):
    st.write("Click the button to get today's activity!")
    if st.button("Get Activity"):
        activities = load_activities()
        activity = random.choice(activities)

        user_data["last_activity_date"] = str(today)
        save_user_data(user_data)

        st.write(f"**Today's activity:** {activity}")
        if st.button("Mark as Done"):
            user_data["points"] += 10
            save_user_data(user_data)
            st.success(f"You've earned 10 points! Total points: {user_data['points']}")
else:
    st.write("You already completed today's activity!")
    st.write(f"Total points: {user_data['points']}")
