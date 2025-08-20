import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from utils.permissions import require_authentication
from utils.timetable_parser import get_room_availability
import config

@require_authentication
def show_page():
    st.title("🏛️ Room Booking System")
    
    # Room selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_room = st.selectbox(
            "Select Room",
            [f"{config.ROOM_PREFIX}-{i:03d}" for i in range(1, config.TOTAL_ROOMS + 1)]
        )
    
    with col2:
        selected_date = st.date_input(
            "Select Date",
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=30)
        )
    
    # Get room availability
    availability = get_room_availability(selected_room, selected_date)
    
    # Display availability
    st.subheader(f"Availability for {selected_room} on {selected_date}")
    
    # Create availability display
    availability_df = pd.DataFrame([
        {
            'Time Slot': slot,
            'Status': 'Available' if availability[slot]['available'] else 'Booked',
            'Booked By': availability[slot].get('booked_by', '-'),
            'Purpose': availability[slot].get('purpose', '-')
        }
        for slot in config.TIME_SLOTS
    ])
    
    # Color code the dataframe
    def highlight_status(val):
        if val == 'Available':
            return 'background-color: #90EE90'
        else:
            return 'background-color: #FFB6C1'
    
    styled_df = availability_df.style.applymap(
        highlight_status, subset=['Status']
    )
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Booking form (only for teachers)
    if st.session_state.user_role == "Teacher":
        st.subheader("Book a Room")
        
        available_slots = [
            slot for slot in config.TIME_SLOTS 
            if availability[slot]['available']
        ]
        
        if available_slots:
            with st.form("booking_form"):
                booking_slot = st.selectbox("Select Time Slot", available_slots)
                purpose = st.text_input("Purpose of Booking")
                additional_info = st.text_area("Additional Information")
                
                submitted = st.form_submit_button("Book Room")
                
                if submitted and purpose:
                    book_room(selected_room, selected_date, booking_slot, 
                             st.session_state.user_email, purpose, additional_info)
                    st.success("Room booked successfully!")
                    st.rerun()
        else:
            st.warning("No available slots for the selected date.")
    else:
        st.info("Only teachers can book rooms. Students can view availability only.")

def book_room(room, date, time_slot, booked_by, purpose, additional_info):
    """Book a room for the specified time slot"""
    try:
        # Load existing bookings
        with open('data/bookings/room_bookings.json', 'r') as f:
            bookings = json.load(f)
    except FileNotFoundError:
        bookings = {}
    
    # Create booking key
    booking_key = f"{room}_{date}_{time_slot}"
    
    # Add booking
    bookings[booking_key] = {
        'room': room,
        'date': str(date),
        'time_slot': time_slot,
        'booked_by': booked_by,
        'purpose': purpose,
        'additional_info': additional_info,
        'booking_time': datetime.now().isoformat()
    }
    
    # Save bookings
    with open('data/bookings/room_bookings.json', 'w') as f:
        json.dump(bookings, f, indent=2)
