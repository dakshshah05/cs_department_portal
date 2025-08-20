import streamlit as st
import hashlib
import json
from pathlib import Path

def show_page():
    """Display login page"""
    st.title("🏫 CS Department Portal")
    st.subheader("Please log in to continue")
    if 'form_instance' not in st.session_state:
        st.session_state.form_instance = 1
    else:
        st.session_state.form_instance += 1
    # Login form
    form_key = f"login_form_{st.session_state.get('form_instance', 'default')}"
    with st.form(form_key):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("University Email", placeholder="your-email@youruni.edu.in")
            password = st.text_input("Password", type="password")
        
        with col2:
            role = st.selectbox("Login as:", ["Student", "Teacher"])
            st.write("")  # Spacing
            st.write("")  # Spacing
            submitted = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if submitted:
            if email and password:
                user = authenticate_user(email, password, role)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_role = role
                    st.session_state.user_name = user['name']
                    st.success(f"Welcome, {user['name']}!")
                    st.rerun()
                
                else:
                    st.error("❌ Invalid credentials or role mismatch!")
            else:
                st.error("Please fill in all fields")
    
    # Demo credentials info
    with st.expander("🔑 Demo Credentials (for testing)"):
        st.write("**Student Login:**")
        st.code("Email: student1@youruni.edu.in\nPassword: student123")
        st.write("**Teacher Login:**") 
        st.code("Email: prof@youruni.edu.in\nPassword: prof123")


def load_users():
    """Load users from JSON file"""
    users_file = Path('data/users.json')
    
    if not users_file.exists():
        # Create initial users for testing
        initial_users = {
            "student1@youruni.edu.in": {
                "password": hashlib.sha256("student123".encode()).hexdigest(),
                "role": "Student",
                "name": "Student One"
            },
            "student2@youruni.edu.in": {
                "password": hashlib.sha256("student123".encode()).hexdigest(), 
                "role": "Student",
                "name": "Student Two"
            },
            "prof@youruni.edu.in": {
                "password": hashlib.sha256("prof123".encode()).hexdigest(),
                "role": "Teacher",
                "name": "Professor Smith"
            },
            "dr.johnson@youruni.edu.in": {
                "password": hashlib.sha256("teacher123".encode()).hexdigest(),
                "role": "Teacher", 
                "name": "Dr. Johnson"
            }
        }
        
        # Create data directory if it doesn't exist
        users_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(users_file, 'w') as f:
            json.dump(initial_users, f, indent=2)
        
        return initial_users
    
    with open(users_file, 'r') as f:
        return json.load(f)

def authenticate_user(email, password, role):
    """Authenticate user credentials"""
    users = load_users()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if email in users:
        user = users[email]
        if user['password'] == password_hash and user['role'] == role:
            return user
    return None

