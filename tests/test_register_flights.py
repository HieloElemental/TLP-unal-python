import pytest
from app.main import flights

@pytest.fixture(autouse=True)
def reset_flights():
    flights.clear()

def test_register_flight_success(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 201
    assert response.json() == flight

def test_register_flight_success_deffault_status(client):
    flight = {
        "flight_number": "FL124",
        "arrival": "New York",
        "departure_time": "2023-10-01T12:00:00Z",
        "gate": "B2"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 201
    assert response.json()["status"] == "Scheduled"

def test_register_flight_failure_empty_request(client):
    response = client.post("/flights/", json={})
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_invalid_json(client):
    response = client.post("/flights/", content="invalid-json")
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_missing_flight_number(client):
    flight = {
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_invalid_flight_number(client):
    flight = {
        "flight_number": "FL#123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_missing_arrival(client):
    flight = {
        "flight_number": "FL123",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_missing_departure_time(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_invalid_departure_time(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "invalid-date",
        "gate": "A1",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_missing_gate(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_invalid_gate(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "InvalidGate",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_invalid_status(client):
    flight = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "InvalidStatus"
    }
    response = client.post("/flights/", json=flight)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_register_flight_failure_duplicate_flight_number(client):
    flight = {
        "flight_number": "NF123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "C3",
        "status": "Scheduled"
    }
    response = client.post("/flights/", json=flight)
    print(response.json())
    assert response.status_code == 201

    response2 = client.post("/flights/", json=flight)
    assert response2.status_code == 422
    assert "detail" in response2.json()

def test_register_flight_failure_gate_used_by_another_flight(client):
    flight1 = {
        "flight_number": "FL123",
        "arrival": "Los Angeles",
        "departure_time": "2023-10-01T10:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    flight2 = {
        "flight_number": "FL456",
        "arrival": "New York",
        "departure_time": "2023-10-01T12:00:00Z",
        "gate": "A1",
        "status": "Scheduled"
    }
    
    response1 = client.post("/flights/", json=flight1)
    assert response1.status_code == 201

    response2 = client.post("/flights/", json=flight2)
    assert response2.status_code == 422
    assert "detail" in response2.json()