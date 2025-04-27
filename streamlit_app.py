import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ----------------------------
# GOOGLE SHEETS CONNECTION
# ----------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)
client = gspread.authorize(credentials)
sheet = client.open("LuckyDrawBookings").worksheet("Sheet1")  # Change to your sheet name if different

# ----------------------------
# FETCH BOOKED NUMBERS
# ----------------------------
bookings = sheet.get_all_records()
booked_numbers = [int(record['Number']) for record in bookings]

# ----------------------------
# STREAMLIT PAGE
# ----------------------------
st.set_page_config(page_title="PK Mobiles Lucky Draw", page_icon="🎉", layout="centered")

st.title("🎉 PK Mobiles Lucky Draw - Book Your Lucky Number")

available_numbers = list(range(1, 51))  # Numbers 1 to 50
cols = st.columns(5)

# Display Numbers in Grid
for i, num in enumerate(available_numbers):
    col = cols[i % 5]
    if num in booked_numbers:
        col.button(f"{num}", disabled=True)
    else:
        if col.button(f"{num}"):
            st.session_state['selected_number'] = num

# ----------------------------
# AFTER NUMBER SELECTION
# ----------------------------
if 'selected_number' in st.session_state:
    selected_number = st.session_state['selected_number']
    
    st.success(f"You selected Number: {selected_number}")
    st.write("Please fill your details to confirm booking:")

    with st.form(key="booking_form", clear_on_submit=True):
        name = st.text_input("Your Name", max_chars=50)
        phone = st.text_input("Phone Number", max_chars=10)
        submit_button = st.form_submit_button("Confirm Booking")
        
        if submit_button:
            # Re-fetch latest booked numbers (in case someone booked meanwhile)
            bookings = sheet.get_all_records()
            booked_numbers = [int(record['Number']) for record in bookings]

            if selected_number in booked_numbers:
                st.error("Oops! This number was just booked by someone else. Please select another.")
                del st.session_state['selected_number']
                st.experimental_rerun()
            else:
                # Save booking
                sheet.append_row([selected_number, name, phone])
                st.success(f"🎉 Congratulations {name}! Your number {selected_number} is booked successfully.")
                
                # Show UPI QR Code (replace with your QR image link)
                st.image("https://your-qr-image-link-here.com/upi_qr.jpg", width=250)  # Replace with your QR code URL
                
                # WhatsApp Group Link
                st.markdown(
                    """
                    **Join our WhatsApp Group for Draw Updates:**  
                    [Join Now](https://chat.whatsapp.com/yourgroupinvitehere)
                    """,
                    unsafe_allow_html=True
                )
                st.balloons()
                
                # Clear selected number to avoid duplicate form
                del st.session_state['selected_number']
                st.stop()
