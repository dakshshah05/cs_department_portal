import os
from dotenv import load_dotenv

load_dotenv()

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///department_portal.db")

# File Upload Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.gif']
ALLOWED_VIDEO_TYPES = ['.mp4', '.avi', '.mov', '.wmv']

# Department Configuration
TOTAL_ROOMS = 30
ROOM_PREFIX = "CS"
DEPARTMENT_EMAIL_DOMAIN = "@youruni.edu.in"

# Time slots
TIME_SLOTS = [
    "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00",
    "16:00-17:00", "17:00-18:00"
]

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
