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

# Function to check and update available numbers
def update_number_status():
    available_numbers = [str(i) for i in range(1, 51) if str(i) not in [booking["Number"] for booking in bookings]]
    booked_numbers = [str(i) for i in range(1, 51) if str(i) in [booking["Number"] for booking in bookings]]
    return available_numbers, booked_numbers

# Function to display numbers as a clickable grid
def display_numbers():
    available_numbers, booked_numbers = update_number_status()

    # Display numbers grid (clickable)
    st.write("### Available Numbers (Green) - Book your numbers")
    number_grid = st.empty()
    
    # Create a clickable grid with numbers and color them based on availability
    col1, col2, col3, col4, col5 = st.columns(5)
    buttons = [col1, col2, col3, col4, col5]
    
    for i, col in enumerate(buttons):
        for j in range(i * 10 + 1, i * 10 + 11):
            if str(j) in booked_numbers:
                col.button(f"{j}", key=f"{j}_booked", disabled=True, help="Booked", use_container_width=True)
            else:
                col.button(f"{j}", key=f"{j}_available", on_click=book_number, args=(j,), use_container_width=True)

    st.write("### Booked Numbers (Red)")
    for i in range(1, 51):
        if str(i) in booked_numbers:
            st.markdown(f"**Number {i}** is **Booked** (Red)")

# Function to book selected number
def book_number(num):
    bookings.append({"Number": str(num)})
    save_bookings(bookings)
    st.success(f"Number {num} booked successfully!")
    st.experimental_rerun()  # Refresh the page to show updated status

# Admin login for reset functionality
admin_password = st.text_input("Admin Password", type="password")
if admin_password == "admin123":  # Use your actual admin password
    st.subheader("Admin Panel")
    reset_button = st.button("Reset All Bookings")
    if reset_button:
        reset_bookings()
else:
    st.warning("You need admin access to reset bookings.")

# Display current booking status
display_numbers()

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
