import pytest
import datetime as dt
from app.main import flights

@pytest.fixture(autouse=True)
def reset_flights():
    flights.clear()
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
        "departure_time": dt.datetime.now() + dt.timedelta(hours=2),
        "gate": "B2",
        "status": "Scheduled"
    })
    flights.append({
        "flight_number": "FL125",
        "arrival": "Chicago",
        "departure_time": dt.datetime.now() + dt.timedelta(hours=1),
        "gate": "C3",
        "status": "Cancelled"
    })
    flights.append({
        "flight_number": "FL126",
        "arrival": "Miami",
        "departure_time": dt.datetime.now() - dt.timedelta(days=3),
        "gate": "D4",
        "status": "Scheduled"
    })

def test_list_flights(client):
    response = client.get("/flights/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert all(dt.datetime.fromisoformat(flight["departure_time"]).day == dt.datetime.now().day for flight in response.json())

def test_list_flights_all_days_filter(client):
    response = client.get("/flights/?departure_time=all")
    assert response.status_code == 200
    assert len(response.json()) == 4

def test_list_flights_scheduled_all_days_filter(client):
    response = client.get("/flights/?flight_status=Scheduled&departure_time=all")
    assert response.status_code == 200
    assert len(response.json()) == 3
    for flight in response.json():
        assert flight["status"] == "Scheduled"

def test_list_flights_date_filter(client):
    otherDay = dt.datetime.now() - dt.timedelta(days=3)
    response = client.get(f"/flights/?flight_status=Scheduled&departure_time={otherDay.isoformat()}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert dt.datetime.fromisoformat(response.json()[0]["departure_time"]).day == otherDay.day

def test_list_flights_invalid_date_filter(client):
    response = client.get("/flights/?flight_status=Scheduled&departure_time=invalid-date")
    assert response.status_code == 422
    assert "detail" in response.json()

def test_list_flights_empty(client):
    flights.clear()
    response = client.get("/flights/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_flights_of_the_day_empty(client):
    flights.clear()
    flights.append({
        "flight_number": "FL127",
        "arrival": "Seattle",
        "departure_time": dt.datetime.now() - dt.timedelta(days=1),
        "gate": "A1",
        "status": "Scheduled"
    })
    response = client.get("/flights/")
    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json() == []

def test_list_flights_with_filter(client):
    response = client.get("/flights/?flight_status=Scheduled")
    assert response.status_code == 200
    flights_data = response.json()
    for flight in flights_data:
        assert flight["status"] == "Scheduled"
    assert len(flights_data) == 2
    for flight in flights_data:
        assert flight["status"] == "Scheduled"

def test_list_flights_with_invalid_filter(client):
    response = client.get("/flights/?flight_status=InvalidStatus")
    assert response.status_code == 422
    assert "detail" in response.json()

def test_list_flights_with_no_filter(client):
    response = client.get("/flights/")
    assert response.status_code == 200
    flights_data = response.json()
    assert len(flights_data) == 3
    for flight in flights_data:
        assert flight["status"] in ["Scheduled", "Cancelled"]