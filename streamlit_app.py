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
st.info("Click on a number to book it!")

# Booking form
with st.form(key="booking_form"):
    name = st.text_input("Enter your Name")
    phone = st.text_input("Enter your Phone Number")
    selected_number = st.session_state.get("selected_number", None)

    if selected_number:
        st.write(f"Selected Number: **{selected_number}**")

    submit = st.form_submit_button("Book Now")

    if submit:
        if not selected_number:
            st.error("Please select a number first!")
        elif selected_number in booked_numbers:
            st.error(f"Number {selected_number} is already booked!")
        elif not name.strip() or not phone.strip():
            st.error("Please enter both Name and Phone Number.")
        else:
            # Save booking
            new_booking = pd.DataFrame({
                "Number": [selected_number],
                "Name": [name],
                "Phone": [phone]
            })
            df = pd.concat([df, new_booking], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Successfully booked number {selected_number}!")
            booked_numbers.add(selected_number)
            # Clear selected number after booking
            st.session_state.selected_number = None
            st.experimental_rerun()

# Show grid of numbers
st.subheader("📋 Available and Booked Numbers:")

cols = st.columns(10)  # 10 columns for grid layout

for i in range(1, 51):
    col = cols[(i-1) % 10]
    if i in booked_numbers:
        col.button(f"{i}\nBooked", disabled=True)
    else:
        if col.button(str(i)):
            st.session_state.selected_number = i

# Admin View (optional, simple password)
with st.expander("🔒 Admin Panel (View Bookings)"):
    admin_password = st.text_input("Enter Admin Password", type="password")
    if admin_password == "pkmobiles123":  # Change password as needed
        st.success("Access Granted ✅")
        st.write("### All Bookings:")
        st.dataframe(df.sort_values("Number"))
    elif admin_password:
        st.error("Incorrect password ❌")
