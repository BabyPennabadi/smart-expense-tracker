import pytest
from fastapi.testclient import TestClient
from src.main import app, expenses_db


@pytest.fixture(autouse=True)
def clear_db():
    """Reset in-memory storage before each test."""
    expenses_db.clear()


client = TestClient(app)


def test_create_expense():
    payload = {
        "title": "Groceries",
        "amount": 45.50,
        "category": "Food",
        "date": "2026-07-30"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Groceries"
    assert data["amount"] == 45.50
    assert data["category"] == "Food"


def test_get_all_expenses():
    client.post("/expenses", json={"title": "Coffee", "amount": 4.0, "category": "Food", "date": "2026-07-30"})
    client.post("/expenses", json={"title": "Bus Ticket", "amount": 2.5, "category": "Transport", "date": "2026-07-30"})

    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_expenses_by_category():
    client.post("/expenses", json={"title": "Lunch", "amount": 12.0, "category": "Food", "date": "2026-07-30"})
    client.post("/expenses", json={"title": "Taxi", "amount": 20.0, "category": "Transport", "date": "2026-07-30"})

    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["title"] == "Lunch"


def test_get_expense_summary():
    client.post("/expenses", json={"title": "Lunch", "amount": 10.0, "category": "Food", "date": "2026-07-30"})
    client.post("/expenses", json={"title": "Dinner", "amount": 20.0, "category": "Food", "date": "2026-07-30"})
    client.post("/expenses", json={"title": "Movie", "amount": 15.0, "category": "Entertainment", "date": "2026-07-30"})

    response = client.get("/expenses/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_total"] == 45.0
    assert data["by_category"]["Food"] == 30.0
    assert data["by_category"]["Entertainment"] == 15.0


def test_delete_expense():
    create_res = client.post("/expenses", json={"title": "Book", "amount": 15.0, "category": "Education", "date": "2026-07-30"})
    expense_id = create_res.json()["id"]

    delete_res = client.delete(f"/expenses/{expense_id}")
    assert delete_res.status_code == 204

    get_res = client.get("/expenses")
    assert len(get_res.json()) == 0


def test_delete_nonexistent_expense():
    response = client.delete("/expenses/invalid-id")
    assert response.status_code == 404
