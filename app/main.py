from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

flights = []

valid_gates = ["A1", "B2", "C3"]
valid_statuses = ["Scheduled", "Awaiting Boarding", "Boarding", "Departing", "Departed", "Delayed", "Cancelled"]

class Flight(BaseModel):
    flight_number: str
    arrival: str
    departure_time: datetime
    gate: str
    status: Optional[str] = "Scheduled"

def flight_number_is_valid(flight_number: str) -> bool:
    if not flight_number.isalnum() or not len(flight_number) <= 10:
        return False
    if not flight_number[0:2].isalpha() or not flight_number[2:].isdigit():
        return False
    return True

@app.post("/flights/", response_model=Flight, status_code=status.HTTP_201_CREATED)
def register_flight(flight: Flight):
    if not flight_number_is_valid(flight.flight_number):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid flight number")
    if flight.gate not in valid_gates:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid gate")
    if flight.status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid status")
    if any(flight.flight_number == f.flight_number for f in flights):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight number already exists")
    if any(f.gate == flight.gate for f in flights if f.status not in ["Departed", "Cancelled"]):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Gate already used by another flight")
    
    flights.append(flight)
    return flight
