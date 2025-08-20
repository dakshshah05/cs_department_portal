import streamlit as st
import hashlib
import json

# Simple user database (in real app, use proper database)
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create initial users
        users = {
            "daksh.kumar@bcah.christuniversity.in": {
                "password": hashlib.sha256("student123".encode()).hexdigest(),
                "role": "Student",
                "name": "John Student"
            },
            "prof@youruni.edu.in": {
                "password": hashlib.sha256("prof123".encode()).hexdigest(),
                "role": "Teacher", 
                "name": "Dr. Smith"
            }
        }
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
        return users

def authenticate_user(email, password):
    users = load_users()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if email in users and users[email]['password'] == password_hash:
        return users[email]
    return None

def login_page():
    st.title("CS Department Portal - Login")
    form_key = f"login_form_{st.session_state.get('form_instance', 'default')}"
    with st.form(form_key):
        email = st.text_input("University Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Login as:", ["Student", "Teacher"])
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = authenticate(email, password)
            if user and user['role'] == role:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_role = role
                st.session_state.user_name = user['name']
                st.rerun()
            else:
                st.error("Invalid credentials or role mismatch")

# Main app logic
if not st.session_state.get('authenticated', False):
    login_page()
else:
    st.title(f"Welcome, {st.session_state.user_name}")
    st.write(f"Role: {st.session_state.user_role}")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.run()
