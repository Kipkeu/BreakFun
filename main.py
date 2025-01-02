import random
import json
import plyer
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

# Function to send notification
def send_notification(message):
    plyer.notification.notify(
        title="Daily Fun Activity!",
        message=message,
        timeout=10
    )

# Main function
def main():
    user_data = load_user_data()
    today = datetime.now().date()

    if user_data.get("last_activity_date") != str(today):
        # Pick a random activity
        activities = load_activities()
        activity = random.choice(activities)

        # Send a notification
        send_notification(activity)

        # Prompt the user to complete the activity
        print(f"Today's activity: {activity}")
        completed = input("Did you complete this activity? (yes/no): ").strip().lower()

        if completed == "yes":
            # Award points if completed
            user_data["last_activity_date"] = str(today)
            user_data["points"] += 10
            save_user_data(user_data)
            print(f"Great job! You earned 10 points. Total points: {user_data['points']}")
        else:
            print("No points awarded. Try completing your activity next time!")

if __name__ == "__main__":
    main()
