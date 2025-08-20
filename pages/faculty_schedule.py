import streamlit as st
import json
import pandas as pd
from utils.permissions import require_authentication
from utils.timetable_parser import get_faculty_schedule
import config

@require_authentication
def show_page():
    st.title("👨‍🏫 Faculty Schedule")
    
    # Load faculty list
    try:
        with open('data/faculty_list.json', 'r') as f:
            faculty_list = json.load(f)
    except FileNotFoundError:
        st.error("Faculty list not found. Please contact administrator.")
        return
    
    # Faculty selection
    selected_faculty = st.selectbox(
        "Select Faculty Member",
        list(faculty_list.keys())
    )
    
    # Get faculty schedule
    schedule = get_faculty_schedule(selected_faculty)
    
    # Display schedule
    st.subheader(f"Schedule for {faculty_list[selected_faculty]['name']}")
    
    # Create schedule dataframe
    schedule_data = []
    for day in config.DAYS_OF_WEEK:
        for time_slot in config.TIME_SLOTS:
            slot_info = schedule.get(day, {}).get(time_slot, {})
            schedule_data.append({
                'Day': day,
                'Time': time_slot,
                'Status': 'Free' if slot_info.get('free', True) else 'Busy',
                'Subject/Activity': slot_info.get('activity', '-'),
                'Room': slot_info.get('room', '-')
            })
    
    # Convert to dataframe
    df = pd.DataFrame(schedule_data)
    
    # Pivot table for better visualization
    pivot_df = df.pivot(index='Time', columns='Day', values='Status')
    
    # Display as heatmap-style table
    def color_status(val):
        if val == 'Free':
            return 'background-color: #90EE90'
        else:
            return 'background-color: #FFB6C1'
    
    st.dataframe(
        pivot_df.style.applymap(color_status),
        use_container_width=True
    )
    
    # Detailed schedule
    with st.expander("Detailed Schedule"):
        st.dataframe(df, use_container_width=True)
    
    # Free slots summary
    free_slots = df[df['Status'] == 'Free']
    if not free_slots.empty:
        st.subheader("Free Slots Summary")
        free_summary = free_slots.groupby('Day').size().reset_index(name='Free Slots')
        st.bar_chart(free_summary.set_index('Day'))
