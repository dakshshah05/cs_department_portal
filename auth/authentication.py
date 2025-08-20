import streamlit as st
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
import config

class GoogleAuthenticator:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": config.GOOGLE_CLIENT_ID,
                "client_secret": config.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [config.REDIRECT_URI]
            }
        }
    
    def get_authorization_url(self):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=['openid', 'email', 'profile']
        )
        flow.redirect_uri = config.REDIRECT_URI
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state
    
    def authenticate_user(self, authorization_code, state):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=['openid', 'email', 'profile'],
            state=state
        )
        flow.redirect_uri = config.REDIRECT_URI
        
        try:
            flow.fetch_token(code=authorization_code)
            credentials = flow.credentials
            
            # Get user info
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            
            return {
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'verified_email': user_info.get('verified_email')
            }
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return None

def determine_user_role(email):
    """Determine if user is student or teacher based on email or other criteria"""
    # You can implement your own logic here
    # For now, using a simple approach based on email patterns
    
    # Load teacher emails from a file or database
    try:
        with open('data/teacher_emails.json', 'r') as f:
            teacher_emails = json.load(f)
        
        if email in teacher_emails:
            return "Teacher"
        else:
            return "Student"
    except FileNotFoundError:
        # Default to student if no teacher list found
        return "Student"
