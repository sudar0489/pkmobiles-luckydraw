import json
import os
import pandas as pd
import streamlit as st

# Path to the bookings JSON file
json_file = "bookings.json"

# Function to reset the bookings file to empty
def reset_bookings():
    empty_data = []  # Empty list to reset bookings
    with open(json_file, 'w') as f:
        json.dump(empty_data, f)
    st.success("Bookings have been reset!")

# Function to check if the file exists and load it
def load_bookings():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            bookings = json.load(f)
        return bookings
    else:
        # If the file does not exist, initialize it as empty
        with open(json_file, 'w') as f:
            json.dump([], f)
        return []

# Load bookings data
bookings = load_bookings()

# Function to save bookings data back to JSON
def save_bookings(bookings):
    with open(json_file, 'w') as f:
        json.dump(bookings, f)

# Display available or booked numbers
def show_numbers():
    available_numbers = [str(i) for i in range(1, 51) if str(i) not in [booking["Number"] for booking in bookings]]
    booked_numbers = [str(i) for i in range(1, 51) if str(i) in [booking["Number"] for booking in bookings]]

    if available_numbers:
        st.write(f"📋 Available Numbers: {', '.join(available_numbers)}")
    else:
        st.write("🚫 All numbers are booked. Contest is closed. Thanks for participating, we will let you know next contest.")

# Function to book numbers
def book_numbers():
    selected_numbers = st.multiselect("Select numbers to book", [str(i) for i in range(1, 51)])
    if st.button("Submit"):
        if not selected_numbers:
            st.warning("Please select at least one number!")
        else:
            # Update bookings with selected numbers
            for num in selected_numbers:
                bookings.append({"Number": num})
            save_bookings(bookings)
            st.success(f"Successfully booked numbers: {', '.join(selected_numbers)}")

# Streamlit app layout
st.title("Lucky Draw Contest")

# Admin login for reset functionality
admin_password = st.text_input("Admin Password", type="password")
if admin_password == "admin123":  # Use your actual admin password
    st.subheader("Admin Panel")
    reset_button = st.button("Reset All Bookings")
    if reset_button:
        reset_bookings()

else:
    st.warning("You need admin access to reset bookings.")

# Show current status of bookings
show_numbers()

# Allow users to book numbers
book_numbers()

# Export booking data to CSV
def export_to_csv(bookings):
    df = pd.DataFrame(bookings)
    df.to_csv('bookings.csv', index=False)
    st.write("📤 Exported bookings to bookings.csv")

# Admin option to export data
if admin_password == "admin123":
    export_button = st.button("Export Bookings as CSV")
    if export_button:
        export_to_csv(bookings)
        st.success("Bookings data has been exported as CSV.")
