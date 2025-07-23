from fastapi import FastAPI, status, HTTPException, Query, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

flights = []
deletion_log = []

valid_gates = ["A1", "B2", "C3", "D4", "E5"]
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

@app.get("/flights/", response_model=List[Flight])
def list_flights(
    flight_status: Optional[str] = Query(None),
    departure_time: Optional[str] = Query(None)
):
    if flight_status and flight_status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid status filter")

    filtered = flights

    if flight_status:
        filtered = [f for f in filtered if (f.status if isinstance(f, Flight) else f["status"]) == flight_status]

    if departure_time:
        if departure_time == "all":
            return filtered
        try:
            dt_filter = datetime.fromisoformat(departure_time)
        except Exception:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid departure_time filter")
        filtered = [
            f for f in filtered
            if (f.departure_time if isinstance(f, Flight) else f["departure_time"]).date() == dt_filter.date()
        ]
        return filtered

    today = datetime.now().date()
    filtered = [
        f for f in filtered
        if (f.departure_time if isinstance(f, Flight) else f["departure_time"]).date() == today
    ]
    return filtered

@app.put("/flights/")
def update_flight_status(
    flight_number: str = Query(...),
    flight_status: str = Query(...)
):
    flight_number = flight_number[0:2].upper() + flight_number[2:]
    if not flight_number_is_valid(flight_number):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid flight number format")
    if flight_status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid status")

    valid_transitions = {
        "Scheduled": ["Scheduled", "Awaiting Boarding", "Delayed", "Cancelled"],
        "Awaiting Boarding": ["Awaiting Boarding", "Boarding", "Delayed", "Cancelled"],
        "Boarding": ["Boarding", "Departing", "Delayed", "Cancelled"],
        "Departing": ["Departing", "Departed"],
        "Departed": ["Departed"],
        "Delayed": ["Delayed", "Awaiting Boarding", "Boarding", "Cancelled"],
        "Cancelled": ["Cancelled"]
    }

    flight = next((f for f in flights if f["flight_number"] == flight_number), None)
    if flight:
        if flight["status"] in valid_transitions and flight_status in valid_transitions[flight["status"]]:
            flight["status"] = flight_status
            return {"status": flight_status}
        else:
            if flight["status"] == "Cancelled":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cancelled flights cannot be rescheduled")
            if flight["status"] == "Departing" or flight["status"] == "Departed":
                if flight_status == "Delayed":
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight cannot be delayed after departing")
                if flight_status == "Cancelled":
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight cannot be cancelled after departing")
                
            if flight_status == "Scheduled":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight was not in Scheduled status")
            if flight_status == "Awaiting Boarding":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight was not in Scheduled status")
            if flight_status == "Boarding":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight was not in Awaiting Boarding status")
            if flight_status == "Departing":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight was not in Boarding status")
            if flight_status == "Departed":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Flight was not in Departing status")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")

@app.delete("/flights/")
def eliminate_flight(
    flight_number: str = Query(...),
    reason: Optional[str] = Query(None)
):
    flight_number = flight_number[0:2].upper() + flight_number[2:]
    if not flight_number_is_valid(flight_number):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid flight number format")
    
    if not reason:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Reason for elimination is required")

    flight = next((f for f in flights if f["flight_number"] == flight_number), None)
    if not flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight {flight_number} not found")

    flights.remove(flight)
    deletion_log.append({
        "flight_number": flight_number,
        "reason": reason
    })
    
    return {"message": f"Flight {flight_number} eliminated successfully"}