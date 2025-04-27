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
st.info("Click on the numbers to book them! You can select multiple numbers.")

# Booking form
with st.form(key="booking_form"):
    name = st.text_input("Enter your Name")
    phone = st.text_input("Enter your Phone Number")

    # Multi-select for numbers (allow multiple)
    available_numbers = [i for i in range(1, 51) if i not in booked_numbers]
    selected_numbers = st.multiselect("Choose Numbers to Book", available_numbers)

    submit = st.form_submit_button("Book Now")

    if submit:
        if not selected_numbers:
            st.error("Please select at least one number!")
        elif not name.strip() or not phone.strip():
            st.error("Please enter both Name and Phone Number.")
        else:
            # Save the bookings
            new_bookings = pd.DataFrame({
                "Number": selected_numbers * len(selected_numbers),
                "Name": [name] * len(selected_numbers),
                "Phone": [phone] * len(selected_numbers)
            })
            df = pd.concat([df, new_bookings], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            booked_numbers.update(selected_numbers)
            st.success(f"Successfully booked numbers {', '.join(map(str, selected_numbers))}!")
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
