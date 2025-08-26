import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.seed import seed
from app.db import Base, engine

# Ensure tables and seed
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
seed()

client = TestClient(app)

def test_list_classes():
    r = client.get('/classes')
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) >= 3
    assert 'available_slots' in data[0]

def test_booking_flow_and_uniqueness():
    classes = client.get('/classes').json()
    class_id = classes[0]['id']

    # book once
    r = client.post('/book', json={
        "class_id": class_id,
        "client_name": "rimon",
        "client_email": "rimon@example.com"
    })
    assert r.status_code == 201
    # try duplicate
    r2 = client.post('/book', json={
        "class_id": class_id,
        "client_name": "rimon",
        "client_email": "rimon@example.com"
    })
    assert r2.status_code == 409

def test_get_bookings_by_email():
    r = client.get('/bookings', params={"email":"rimon@example.com"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert data[0]['client_email'] == 'rimon@example.com'
