import streamlit as st
from functools import wraps

def require_authentication(func):
    """Decorator to require authentication for a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("Please log in to access this page.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_teacher_role(func):
    """Decorator to require teacher role for a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if st.session_state.get('user_role') != 'Teacher':
            st.error("This feature is only available to teachers.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def check_user_role():
    """Check and return current user role"""
    return st.session_state.get('user_role', None)

def can_write():
    """Check if current user has write permissions"""
    return st.session_state.get('user_role') == 'Teacher'

def can_read():
    """Check if current user has read permissions"""
    return st.session_state.get('authenticated', False)
