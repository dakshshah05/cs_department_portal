import streamlit as st
from auth.authentication import authenticate_user
from pages.login import show_page
from pages import login, room_booking, faculty_schedule, media_gallery
from utils.permissions import check_user_role
import config

# Page configuration
st.set_page_config(
    page_title="CS Department Portal",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open('static/css/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    load_css()
    
    # Initialize session state keys once
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.user_email = None
        st.session_state.show_login_form = True  # New flag
    
    if not st.session_state.authenticated and st.session_state.show_login_form:
        st.session_state.show_login_form = False  # Ensure form renders only once per run
        show_page()
    elif st.session_state.authenticated:
        show_main_app()

def show_main_app():
    st.sidebar.title("CS Department Portal")
    st.sidebar.write(f"Welcome, {st.session_state.user_email}")
    st.sidebar.write(f"Role: {st.session_state.user_role}")
    
    # Navigation
    pages = {
        "Room Booking": room_booking,
        "Faculty Schedule": faculty_schedule,
        "Media Gallery": media_gallery
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.user_email = None
        st.rerun()
    
    # Load selected page
    pages[selected_page].show_page()

if __name__ == "__main__":
    main()
