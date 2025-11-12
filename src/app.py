from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
import threading

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

activities: Dict[str, Dict[str, Any]] = {
    "soccer": {"name": "Soccer", "participants": [], "max_participants": 22, "description": "Partidos y entrenamientos de fútbol."},
    "volleyball": {"name": "Volleyball", "participants": [], "max_participants": 18, "description": "Entrenamientos y torneos de voleibol."},
    "music": {"name": "Music", "participants": [], "max_participants": 30, "description": "Clases y ensayos musicales."},
    "dance": {"name": "Dance", "participants": [], "max_participants": 25, "description": "Taller de danza y coreografías."},
    "math_club": {"name": "Math Club", "participants": [], "max_participants": 40, "description": "Resolución de problemas y competiciones matemáticas."},
    "science_club": {"name": "Science Club", "participants": [], "max_participants": 35, "description": "Proyectos y experimentos científicos."},
    "basketball": {"name": "Basketball", "participants": [], "max_participants": 20, "description": "Partidos y entrenamientos de baloncesto."},
    "swimming": {"name": "Swimming", "participants": [], "max_participants": 30, "description": "Clases y práctica de natación."},
    "painting": {"name": "Painting", "participants": [], "max_participants": 15, "description": "Taller de pintura y técnicas artísticas."},
    "theater": {"name": "Theater", "participants": [], "max_participants": 25, "description": "Grupo de teatro y montaje de obras."},
    "chess": {"name": "Chess Club", "participants": [], "max_participants": 30, "description": "Club de ajedrez: partidas, torneos y enseñanza."},
    "robotics": {"name": "Robotics", "participants": [], "max_participants": 20, "description": "Club de robótica y retos tecnológicos."}
}

activities_lock = threading.Lock()

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities():
    return {
        name: {
            "name": data["name"],
            "participants_count": len(data["participants"]),
            "max_participants": data.get("max_participants"),
            "description": data.get("description", "")
        }
        for name, data in activities.items()
    }

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    with activities_lock:
        activity = activities[activity_name]
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up")

        max_p = activity.get("max_participants")
        if max_p is not None and len(activity["participants"]) >= max_p:
            raise HTTPException(status_code=400, detail="Activity is full")

        activity["participants"].append(email)

    return {"message": f"Signed up {email} for {activity_name}"}
