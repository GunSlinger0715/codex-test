import requests

BASE = "https://jsonplaceholder.typicode.com"

def test_post_1_has_title():
    r = requests.get(f"{BASE}/posts/1", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert "title" in data and isinstance(data["title"], str)

def test_nonexistent_post_returns_404():
    r = requests.get(f"{BASE}/posts/999999", timeout=10)
    assert r.status_code == 404
