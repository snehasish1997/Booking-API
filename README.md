# Booking API (FastAPI)

A small booking API for a fitness studio.

## Tech
- Python 3.11+
- FastAPI + Uvicorn
- SQLite (file DB) via SQLAlchemy
- Pydantic validation
- Timezone support using IANA tz names (default: Asia/Kolkata)

## Run locally

```bash
python -m venv books && source books/bin/activate  # i am using macOS
pip install -r requirements.txt

# Initialize/seed DB
python -c "from app.seed import seed; seed()"

# Start server
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive Swagger.

## Endpoints

### GET /classes
List upcoming classes. Converting start times to any timezone with `tz` query parameter.

Example:
```bash
curl 'http://127.0.0.1:8000/classes?tz=Europe/London'
```

Response (truncated):
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Asha",
    "start_time": "2025-08-25T05:30:00+01:00",
    "timezone": "Europe/London",
    "capacity": 10,
    "available_slots": 9
  }
]
```

### POST /book
Create a booking if slots are available. Each email can book a given class only once.

```bash
curl -X POST http://127.0.0.1:8000/book \
  -H 'Content-Type: application/json' \
  -d '{
    "class_id": 1,
    "client_name": "rimon",
    "client_email": "rimon@example.com"
  }'
```

Possible errors:
- `404` – class not found
- `409` – class is full OR already booked with that email
- `422` – validation error (missing/invalid fields)

### GET /bookings?email=alice@example.com
Return all bookings for a specific email.

```bash
curl 'http://127.0.0.1:8000/bookings?email=rimon@example.com'
```

## Timezone notes
Class times are seeded in IST and stored in UTC in the DB. The `tz` parameter converts to any IANA timezone.
If `tz` is invalid, the API falls back to IST.

## Tests
```bash
pytest -q
```

## Project layout
```
omnify-booking-api/
  app/
    db.py
    models.py
    schemas.py
    utils.py
    main.py
    seed.py
  tests/
    test_main.py
  requirements.txt
  README.md
```

---
