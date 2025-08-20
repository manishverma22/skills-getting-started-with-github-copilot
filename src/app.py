"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")

    # Validate max participants not exceeded
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Maximum participants reached")

    # Add student to the activity
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}    
@app.get("/activities/{activity_name}")
def get_activity_details(activity_name: str):
    """Get details of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activities[activity_name]

@app.get("/activities/{activity_name}/participants")
def get_activity_participants(activity_name: str):
    """Get participants of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activities[activity_name]["participants"]

@app.get("/activities/{activity_name}/schedule")
def get_activity_schedule(activity_name: str):
    """Get schedule of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"schedule": activities[activity_name]["schedule"]}

@app.get("/activities/{activity_name}/description")     
def get_activity_description(activity_name: str):
    """Get description of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"description": activities[activity_name]["description"]}

@app.get("/activities/{activity_name}/max_participants")
def get_activity_max_participants(activity_name: str):
    """Get maximum participants for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"max_participants": activities[activity_name]["max_participants"]}

@app.get("/activities/{activity_name}/current_participants")
def get_activity_current_participants(activity_name: str):
    """Get current participants for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"current_participants": len(activities[activity_name]["participants"])}
