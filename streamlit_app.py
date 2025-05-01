import streamlit as st
import pandas as pd

st.set_page_config(page_title="PK Mobiles Lucky Draw", layout="centered")

# App Variables
TOTAL_COST = 300
COMMISSION_RATE = 0.10
UPI_ID = "pkmobiles2019@oksbi"
GPAY_NO = "+91 98408 69567"
ADMIN_PASSWORD = "prem1988"

# Session state
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

if "name" not in st.session_state:
    st.session_state.name = ""

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "txn_id" not in st.session_state:
    st.session_state.txn_id = ""

if "has_booked" not in st.session_state:
    st.session_state.has_booked = False

if "selected_number" not in st.session_state:
    st.session_state.selected_number = None

# Title & Instructions
st.markdown(f"""
## 🎉 Welcome to the PK Mobiles Lucky Draw! 🎉

Pay just **Rs. 6** and stand a chance to **WIN a ₹300 product!**  
Only **50 spots** available — each person can join **only ONCE** with a **unique mobile number & transaction ID**.

🏆 Winner gets the ₹300 product by paying just Rs. 6 + Rs. 30 (10% service charge)!  
📢 Winner will be announced **TOMORROW** in our **WhatsApp group**.

---

### 👉 [Click here to Pay ₹6](upi://pay?pa={UPI_ID}&pn=PKMobiles&cu=INR)  

---

📌 **Terms & Conditions:**
- One entry per person (based on mobile number + transaction ID)
- Already booked numbers are **not available** again
- Game is conducted with 100% transparency
- Winner will be chosen randomly and announced in our WhatsApp group

🎯 Hurry! Only 50 numbers are available. Grab your lucky spot now!
""")

# Admin view
admin_access = st.text_input("Admin Access", type="password", label_visibility="collapsed")

if admin_access == ADMIN_PASSWORD:
    st.subheader("🔐 Admin View - Bookings")
    if st.session_state.bookings:
        df = pd.DataFrame.from_dict(st.session_state.bookings, orient="index")
        st.dataframe(df)
        csv = df.to_csv(index=True)
        st.download_button("⬇️ Download as CSV", csv, "bookings.csv", "text/csv")
        if st.button("❌ Reset All Bookings"):
            st.session_state.bookings = {}
            st.success("All bookings have been reset.")
    else:
        st.info("No bookings yet.")
    st.stop()

# Booking form
st.markdown("---")
st.subheader("📥 Enter Your Details")

with st.form("details_form"):
    name = st.text_input("👤 Your Name").strip()
    phone = st.text_input("📞 10-digit Phone Number").strip()
    txn_id = st.text_input("💳 Transaction ID").strip()
    details_submit = st.form_submit_button("➡️ Proceed")

# Validate and show number grid
if details_submit:
    already_booked = any(
        entry["Transaction ID"].lower() == txn_id.lower() or entry["Phone"] == phone
        for entry in st.session_state.bookings.values()
    )
    if already_booked:
        st.warning("This transaction ID or phone number has already been used. Thank you for participating.")
        st.stop()

    if not name or len(phone) != 10 or not phone.isdigit() or len(txn_id) < 6:
        st.error("Please fill in valid details to proceed.")
        st.stop()

    st.session_state.name = name
    st.session_state.phone = phone
    st.session_state.txn_id = txn_id
    st.session_state.has_booked = False

# Number selection
if st.session_state.name and not st.session_state.has_booked:
    st.markdown("### 🔢 Choose Your Lucky Number")

    booked_numbers = st.session_state.bookings.keys()

    for row in range(5):
        cols = st.columns(10)
        for col_index in range(10):
            number = row * 10 + col_index + 1
            if number > 50:
                break
            if number in booked_numbers:
                cols[col_index].button(f"#{number}", disabled=True, key=f"num_{number}", use_container_width=True)
            else:
                if cols[col_index].button(f"#{number}", key=f"num_{number}", use_container_width=True):
                    st.session_state.bookings[number] = {
                        "Name": st.session_state.name,
                        "Phone": st.session_state.phone,
                        "Transaction ID": st.session_state.txn_id
                    }
                    st.session_state.has_booked = True
                    st.session_state.selected_number = number
                    st.success(f'✅ Your booking number is "**{number}**". Thank you for participating 🎉')
                    st.rerun()

# Show final confirmation if already booked
if st.session_state.has_booked and st.session_state.selected_number:
    st.success(f'✅ Your booking number is "**{st.session_state.selected_number}**". Thank you for participating 🎉')

# If all numbers booked
if len(st.session_state.bookings) >= 50:
    st.markdown("## ❌ All 50 numbers have been booked. Contest is now closed.")
    st.info("We will inform you about the next contest soon. Thank you for participating!")
