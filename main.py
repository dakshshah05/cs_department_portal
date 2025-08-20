import streamlit as st
from auth.authentication import authenticate_user
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
    
    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

    # Authentication check
    if not st.session_state.authenticated:
        login.show_login_page()
    else:
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
