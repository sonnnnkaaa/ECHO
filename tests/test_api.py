# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# ── AUTH ──────────────────────────────────────────────
def test_register():
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_register_duplicate_email():
    client.post("/api/auth/register", json={
        "email": "dup@example.com",
        "username": "dupuser",
        "password": "testpass123"
    })
    response = client.post("/api/auth/register", json={
        "email": "dup@example.com",
        "username": "dupuser2",
        "password": "testpass123"
    })
    assert response.status_code == 400

def test_login():
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "testpass123"
    })
    response = client.post("/api/auth/login", data={
        "username": "loginuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/api/auth/login", data={
        "username": "loginuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401

# ── CHECKLISTS ────────────────────────────────────────
@pytest.fixture
def auth_token():
    client.post("/api/auth/register", json={
        "email": "check@example.com",
        "username": "checkuser",
        "password": "testpass123"
    })
    response = client.post("/api/auth/login", data={
        "username": "checkuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]

def test_create_checklist(auth_token):
    response = client.post("/api/checklists/", 
        json={
            "title": "Test Checklist",
            "description": "Test description",
            "categories": []
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Checklist"

def test_get_checklists():
    response = client.get("/api/checklists/")
    assert response.status_code == 200
    assert "checklists" in response.json()

def test_get_checklist_not_found():
    response = client.get("/api/checklists/99999")
    assert response.status_code == 404

def test_create_checklist_unauthorized():
    response = client.post("/api/checklists/", json={
        "title": "Test",
        "description": "Test",
        "categories": []
    })
    assert response.status_code == 401