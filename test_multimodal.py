import pytest
import requests
import json
import time
import subprocess
import os
import signal

@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Start the Flask server
    proc = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start
    yield
    # Kill the server
    os.kill(proc.pid, signal.SIGTERM)

def test_submit_alt_text_ai():
    url = "http://127.0.0.1:5000/submit"
    # Formulaic AI description
    payload = {
        "text": "A photo of a sunset over the mountains with high-quality resolution and detailed lens flare.",
        "creator_id": "creator_123",
        "content_type": "image_description"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "image_description"
    assert "template_score" in data
    assert "verbosity_score" in data
    # Should lean towards AI due to "A photo of" template and clinical detail
    assert data["template_score"] >= 0.7

def test_submit_alt_text_human():
    url = "http://127.0.0.1:5000/submit"
    # Subjective human description
    payload = {
        "text": "The golden light hits the jagged peaks just right, reminding me of our trip last summer.",
        "creator_id": "creator_456",
        "content_type": "image_description"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "image_description"
    # Should have low template conformity
    assert data["template_score"] <= 0.3
    # Human description is likely 'likely_human' or 'uncertain' but definitely not high confidence AI
    assert data["attribution"] != "likely_ai"

def test_submit_standard_text_regression():
    url = "http://127.0.0.1:5000/submit"
    payload = {
        "text": "This is a standard long-form text submission to ensure that the primary pipeline still works correctly after the multi-modal refactor. It contains enough words to satisfy stylometric checks and should be classified appropriately.",
        "creator_id": "creator_789"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["content_type"] == "text"
    assert "stylo_score" in data
    assert "template_score" not in data
