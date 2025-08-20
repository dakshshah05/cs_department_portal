def get_room_availability(room_name, date):
    """
    Returns availability of the room for the given date.
    Replace this stub with your actual timetable parsing logic.
    """
    # Dummy example returning all slots available
    time_slots = [
        "08:00-09:00", "09:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00",
        "14:00-15:00", "15:00-16:00", "16:00-17:00",
        "17:00-18:00"
    ]
    availability = {}
    for slot in time_slots:
        availability[slot] = {"available": True}
    return availability
def get_faculty_schedule(faculty_email):
    """
    Returns the schedule for a given faculty email.
    Replace with actual logic to read from your timetable data files.
    """

    import json
    from pathlib import Path

    schedule_file = Path('data/timetables/faculty_schedule.json')
    if not schedule_file.exists():
        return {}

    with open(schedule_file, 'r') as f:
        faculty_schedules = json.load(f)

    # Return schedule for the faculty or empty dict if not found
    return faculty_schedules.get(faculty_email, {})
