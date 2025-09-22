import pytest
from app import app

# ใช้ test client ของ Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_plus(client):
    # ทดสอบ 5 + 6 = 11
    response = client.get("/plus/5/6")
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 11

    # ทดสอบ 0 + 0 = 0
    response = client.get("/plus/0/0")
    data = response.get_json()
    assert data["result"] == 0

    # ทดสอบตัวเลขติดลบ -3 + 7 = 4
    response = client.get("/plus/-3/7")
    data = response.get_json()
    assert data["result"] == 4
