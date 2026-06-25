import pytest
import subprocess
import time
import os
import signal
import requests
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module", autouse=True)
def server():
    proc = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    yield
    os.kill(proc.pid, signal.SIGTERM)

def test_full_pipeline():
    # 1. Test Submission
    print("Testing Submission...")
    payload = {
        "text": "The sun dipped below the horizon, painting the sky in hues of amber and rose. I sat on the porch, coffee in hand, watching the neighborhood slowly go quiet.",
        "creator_id": "user-123"
    }
    resp = requests.post("http://localhost:5000/submit", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    content_id = data['content_id']

    # 2. Test Appeal
    print("Testing Appeal...")
    appeal_payload = {
        "content_id": content_id,
        "creator_reasoning": "This is my personal writing."
    }
    resp = requests.post("http://localhost:5000/appeal", json=appeal_payload)
    assert resp.status_code == 200

    # 3. Test Dashboard (Admin)
    print("Testing Dashboard...")
    headers = {"X-Admin-Key": "super-secret-admin-key"}
    resp = requests.get("http://localhost:5000/dashboard", headers=headers)
    assert resp.status_code == 200
    stats = resp.json()
    assert stats['total'] >= 1
    assert stats['appeal_count'] >= 1

    print("System Verification Successful!")

if __name__ == "__main__":
    pytest.main([__file__])
