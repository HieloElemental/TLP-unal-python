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

def test_scheduled_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 200
    assert response.json()["status"] == "Scheduled"

def test_scheduled_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"

def test_scheduled_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Awaiting Boarding status"}

def test_scheduled_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Boarding status"}

def test_scheduled_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Departing status"}

def test_scheduled_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"

def test_scheduled_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"

def test_awaiting_boarding_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_awaiting_boarding_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_awaiting_boarding_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"

def test_awaiting_boarding_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Boarding status"}

def test_awaiting_boarding_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Departing status"}

def test_awaiting_boarding_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"

def test_awaiting_boarding_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"

def test_boarding_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_boarding_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_boarding_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"

def test_boarding_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"

def test_boarding_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Departing status"}

def test_boarding_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"

def test_boarding_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"

def test_departing_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_departing_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_departing_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Awaiting Boarding status"}

def test_departing_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"

def test_departing_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"

def test_departing_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight cannot be delayed after departing"}

def test_departing_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight cannot be cancelled after departing"}

def test_departed_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_departed_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_departed_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Awaiting Boarding status"}

def test_departed_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Departing status"}

def test_departed_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"

def test_departed_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight cannot be delayed after departing"}

def test_departed_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 200
    assert response.json()["status"] == "Departing"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 200
    assert response.json()["status"] == "Departed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight cannot be cancelled after departing"}

def test_delayed_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_delayed_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Awaiting Boarding"

def test_delayed_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 200
    assert response.json()["status"] == "Boarding"

def test_delayed_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Boarding status"}

def test_delayed_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Departing status"}

def test_delayed_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"

def test_delayed_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 200
    assert response.json()["status"] == "Delayed"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"

def test_cancelled_to_scheduled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_awaiting_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Awaiting%20Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_boarding(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Boarding")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_departing(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departing")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_departed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Departed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_delayed(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Delayed")
    assert response.status_code == 422
    assert response.json() == {"detail": "Cancelled flights cannot be rescheduled"}

def test_cancelled_to_cancelled(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Cancelled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Flight was not in Scheduled status"}

def test_flight_not_found(client):
    flight_number = "FL999"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 404
    assert response.json() == {"detail": "Flight not found"}

def test_invalid_status(client):
    flight_number = "FL123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=InvalidStatus")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid flight status"}

def test_invalid_flight_number(client):
    flight_number = "FL@123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid flight number format"}

def test_flight_number_case_insensitive(client):
    flight_number = "fl123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 200
    assert response.json()["status"] == "Scheduled"

def test_flight_number_with_spaces(client):
    flight_number = "FL 123"
    response = client.put(f"/flights/?flight_number={flight_number}&status=Scheduled")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid flight number format"}

