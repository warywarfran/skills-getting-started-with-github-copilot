from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Datos de ejemplo
activities = {
    "running": {
        "participants": ["alice@example.com", "bob@example.com"],
        "description": "Running activity"
    },
    "swimming": {
        "participants": ["alice@example.com", "bob@example.com"],
        "description": "Swimming activity"
    }
}

@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activities[activity_name]

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    # Validar que la actividad exista
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Obtener y normalizar la lista de participantes
    participants = activities[activity_name].get("participants")
    if isinstance(participants, str):
        participants = [participants]
        activities[activity_name]["participants"] = participants
    elif participants is None:
        participants = []
        activities[activity_name]["participants"] = participants

    # Validar que el estudiante no esté ya registrado
    if email in participants:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Añadir estudiante
    participants.append(email)
    return {"message": f"Signed up {email} for {activity_name}"}