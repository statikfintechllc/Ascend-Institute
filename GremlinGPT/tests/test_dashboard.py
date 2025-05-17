import requests

def test_backend_api():
    res = requests.get("http://localhost:5050/")
    assert res.status_code == 200
    assert "GremlinGPT" in res.text or "Backend" in res.text

def test_chat_handler():
    res = requests.post("http://localhost:5050/api/chat", json={"text": "scan penny stocks"})
    assert res.status_code == 200
    assert "response" in res.json()

