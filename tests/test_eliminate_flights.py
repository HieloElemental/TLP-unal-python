import pytest
import datetime as dt
from app.main import flights
from app.main import deletion_log

@pytest.fixture(autouse=True)
def reset_flights():
    flights.clear()
    deletion_log.clear()
    flights.append({
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": dt.datetime.now(),
        "gate": "A1",
        "status": "Scheduled"
    })
    flights.append({
        "flight_number": "FL124",
        "arrival": "New York",
        "departure_time": dt.datetime.now(),
        "gate": "B2",
        "status": "Scheduled"
    })
    flights.append({
        "flight_number": "FL125",
        "arrival": "Chicago",
        "departure_time": dt.datetime.now(),
        "gate": "C3",
        "status": "Cancelled"
    })
    flights.append({
        "flight_number": "FL126",
        "arrival": "Miami",
        "departure_time": dt.datetime.now(),
        "gate": "D4",
        "status": "Scheduled"
    })

def test_eliminate_flight_success(client):
    flight_number = "FL123"
    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 200
    assert response.json() == {"message": f"Flight {flight_number} eliminated successfully"}
    assert not any(flight["flight_number"] == flight_number for flight in flights)
    assert any(log["flight_number"] == flight_number for log in deletion_log)
    assert deletion_log[0]["reason"] == "Test elimination"

def test_eliminate_flight_not_found(client):
    flight_number = "FL999"
    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Flight {flight_number} not found"}

def test_eliminate_flight_no_reason(client):
    flight_number = "FL124"
    response = client.delete(f"/flights/?flight_number={flight_number}")
    assert response.status_code == 422
    assert response.json() == {"detail": "Reason for elimination is required"}

def test_eliminate_flight_invalid_flight_number(client):
    flight_number = "FL#124"
    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid flight number format"}

def test_eliminate_flight_already_eliminated(client):
    flight_number = "FL125"
    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 200
    assert not any(flight["flight_number"] == flight_number for flight in flights)
    assert any(log["flight_number"] == flight_number for log in deletion_log)
    assert deletion_log[0]["reason"] == "Test elimination"

    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Flight {flight_number} not found"}

def test_eliminate_flight_empty_flights(client):
    flights.clear()
    flight_number = "FL123"
    response = client.delete(f"/flights/?flight_number={flight_number}&reason=Test%20elimination")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Flight {flight_number} not found"}
