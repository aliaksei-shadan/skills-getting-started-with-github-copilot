import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Chess Club" in response.json()["message"]
    # Проверяем, что участник добавлен
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]

def test_unregister_participant():
    email = "newstudent@mergington.edu"
    # Сначала добавим участника
    client.post(f"/activities/Programming Class/signup?email={email}")
    # Теперь удалим
    response = client.post(f"/activities/Programming Class/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from Programming Class" in response.json()["message"]
    # Проверяем, что участник удалён
    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_participant_not_found():
    response = client.post("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
