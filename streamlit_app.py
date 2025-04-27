import streamlit as st

# Initialize session state for bookings
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

# App title
st.title("🎉 PK Mobiles Lucky Draw Contest")

# Instructions
st.info("Select your number, enter your name and phone number to book!")

# Input form
with st.form(key="booking_form"):
    name = st.text_input("Enter your Name")
    phone = st.text_input("Enter your Phone Number")
    selected_number = st.number_input("Choose a Number (1-50)", min_value=1, max_value=50, step=1)
    submit = st.form_submit_button("Book Now")

    if submit:
        if selected_number in st.session_state.bookings:
            st.error(f"Number {selected_number} is already booked! Please choose another.")
        elif not name.strip() or not phone.strip():
            st.error("Please enter both Name and Phone Number.")
        else:
            # Save the booking
            st.session_state.bookings[selected_number] = {"name": name, "phone": phone}
            st.success(f"Successfully booked number {selected_number}!")

# Show grid of numbers
st.subheader("📋 Available and Booked Numbers:")

cols = st.columns(10)  # 10 columns for grid layout
for i in range(1, 51):
    col = cols[(i-1) % 10]
    if i in st.session_state.bookings:
        col.button(f"{i} - Booked", disabled=True)
    else:
        col.button(str(i))

# Admin View (optional, simple password)
with st.expander("🔒 Admin Panel (View Bookings)"):
    admin_password = st.text_input("Enter Admin Password", type="password")
    if admin_password == "pkmobiles123":  # You can change this password
        st.success("Access Granted ✅")
        st.write("### All Bookings:")
        st.table([
            {"Number": num, "Name": details["name"], "Phone": details["phone"]}
            for num, details in sorted(st.session_state.bookings.items())
        ])
    elif admin_password:
        st.error("Incorrect password ❌")
