import streamlit as st
import pandas as pd
import os

# File to store bookings
DATA_FILE = "bookings.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Number", "Name", "Phone"])
    df.to_csv(DATA_FILE, index=False)

# Load existing bookings
df = pd.read_csv(DATA_FILE)

# Create a set of booked numbers
booked_numbers = set(df["Number"].tolist())

# App title
st.title("🎉 PK Mobiles Lucky Draw Contest")

# Instructions
st.info("Click on the boxes below to book the numbers. You can select multiple numbers.")

# Booking form
with st.form(key="booking_form"):
    name = st.text_input("Enter your Name")
    phone = st.text_input("Enter your Phone Number")
    
    # Store selected numbers in session state
    selected_numbers = st.session_state.get("selected_numbers", [])

    # Display selected numbers
    if selected_numbers:
        st.write(f"Selected Numbers: {', '.join(map(str, selected_numbers))}")
    
    submit = st.form_submit_button("Book Now")

    if submit:
        if not selected_numbers:
            st.error("Please select at least one number!")
        elif not name.strip() or not phone.strip():
            st.error("Please enter both Name and Phone Number.")
        else:
            # Save the bookings
            new_bookings = pd.DataFrame({
                "Number": selected_numbers,
                "Name": [name] * len(selected_numbers),
                "Phone": [phone] * len(selected_numbers)
            })
            df = pd.concat([df, new_bookings], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            booked_numbers.update(selected_numbers)
            st.success(f"Successfully booked numbers {', '.join(map(str, selected_numbers))}!")
            st.session_state.selected_numbers = []  # Clear selected numbers

# Show grid of numbers (Clickable Boxes)
st.subheader("📋 Available and Booked Numbers:")

# Ensure the numbers are sorted in ascending order
all_numbers = list(range(1, 51))
sorted_numbers = sorted(all_numbers)

cols = st.columns(10)  # 10 columns for grid layout

# Check if all numbers are booked
if len(booked_numbers) == len(all_numbers):
    st.warning("🚫 All numbers are booked. Contest is closed. Thanks for participating, we will let you know next contest.")
else:
    # Update the booked numbers and display clickable boxes
    for i in sorted_numbers:
        col = cols[(i-1) % 10]
        
        # Set color based on the booking status
        if i in booked_numbers:
            color = "red"  # Booked numbers will be red
            disabled = True
        else:
            color = "green"  # Available numbers will be green
            disabled = False
        
        # Create a clickable button for each number
        if col.button(f"{i}", key=f"number_{i}", disabled=disabled, use_container_width=True):
            # Toggle the number in the selected numbers list
            if i not in selected_numbers:
                selected_numbers.append(i)
            else:
                selected_numbers.remove(i)
            st.session_state.selected_numbers = selected_numbers

# Admin View (optional, simple password)
with st.expander("🔒 Admin Panel (View Bookings)"):

    admin_password = st.text_input("Enter Admin Password", type="password")
    
    # Check if the entered password matches the predefined one
    correct_password = "prem1988"  # Changed password
    if admin_password == correct_password:
        st.success("Access Granted ✅")
        st.write("### All Bookings:")
        st.dataframe(df.sort_values("Number"))
        
        # Export the data as a downloadable CSV file
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="bookings.csv",
            mime="text/csv"
        )

        # Revoke bookings (Admin only)
        with st.form(key="revoke_form"):
            revoke_number = st.number_input("Enter number to revoke", min_value=1, max_value=50)
            revoke_button = st.form_submit_button("Revoke Booking")

            if revoke_button:
                if revoke_number in booked_numbers:
                    booked_numbers.remove(revoke_number)
                    df = df[df["Number"] != revoke_number]  # Remove the revoked number's booking
                    df.to_csv(DATA_FILE, index=False)
                    st.success(f"Booking for number {revoke_number} has been revoked.")
                else:
                    st.error(f"Number {revoke_number} is not booked.")

        # Reset button for clearing the bookings
        if st.button("Reset All Bookings"):
            confirmation = st.checkbox("Are you sure you want to reset all bookings?")
            if confirmation:
                # Clear bookings in the CSV and update the set
                df = pd.DataFrame(columns=["Number", "Name", "Phone"])
                df.to_csv(DATA_FILE, index=False)
                booked_numbers.clear()
                st.success("All bookings have been reset.")
                
    elif admin_password:
        st.error("Incorrect password ❌")
