import pytest
import subprocess
import time
import os
import signal
import json
import requests
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module", autouse=True)
def server():
    # Kill any existing process on port 5000
    try:
        subprocess.run(["fuser", "-k", "5000/tcp"], check=False)
    except:
        pass

    # Initialize DB
    subprocess.run(["python", "init_db.py"], check=True)

    proc = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Poll until server is up
    start_time = time.time()
    while time.time() - start_time < 20:
        try:
            requests.get("http://127.0.0.1:5000/dashboard", headers={"X-Admin-Key": "super-secret-admin-key"})
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        # If we timed out, print server logs
        stdout, stderr = proc.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
        pytest.fail("Server failed to start")

    yield
    os.kill(proc.pid, signal.SIGTERM)

def test_system_comprehensive():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Create a context that records video
        video_path = "videos/"
        if not os.path.exists(video_path):
            os.makedirs(video_path)

        context = browser.new_context(
            record_video_dir=video_path,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        request_context = context.request

        # Helper to log to the page so it appears in the video
        def log(msg):
            print(msg)
            safe_msg = json.dumps(msg)
            page.evaluate(f"document.body.innerHTML += '<p style=\"font-family: monospace; font-size: 14px; margin: 5px; white-space: pre-wrap;\">' + {safe_msg} + '</p>'")

        page.goto("about:blank")
        page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#cccccc'; document.body.style.padding = '20px';")
        log("Elite Engineering SDLC: Live TDD Verification Session")
        log("Project: Provenance Guard")
        log("=====================================================")

        # 1. Label Mapping Verification
        log("\n[1/4] Testing Label Mapping (AI, Human, Uncertain)")
        samples = {
            "AI": "Artificial intelligence represents a transformative paradigm shift in modern society. It is important to note that while the benefits of AI are numerous, it is equally essential to consider the ethical implications. Furthermore, stakeholders across various sectors must collaborate to ensure responsible deployment.",
            "Human": "ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably won't go back unless someone drags me there",
            "Uncertain": "I've been thinking a lot about remote work lately. There are genuine tradeoffs — flexibility and no commute on one side, isolation and blurred work-life boundaries on the other. Studies show productivity varies widely by individual and role type."
        }

        results = {}
        for name, text in samples.items():
            resp = request_context.post("http://127.0.0.1:5000/submit", data={
                "text": text,
                "creator_id": f"test-user-{name}"
            })
            assert resp.status == 200
            data = resp.json()
            results[name] = data
            log(f"-> Sample {name}: Confidence={data['confidence']}, Attribution={data['attribution']}")
            log(f"   Label: {data['label']}")

        # 2. Appeal Workflow Verification
        log("\n[2/4] Testing Appeal Workflow")
        # Use the content_id from the Human sample
        content_id = results['Human']['content_id']
        appeal_resp = request_context.post("http://127.0.0.1:5000/appeal", data={
            "content_id": content_id,
            "creator_reasoning": "This is definitely my personal writing about my lunch experience."
        })
        assert appeal_resp.status == 200
        appeal_data = appeal_resp.json()
        assert appeal_data['status'] == "under_review"
        log(f"-> Appeal submitted for {content_id}")
        log(f"-> Status: {appeal_data['status']}")
        log(f"-> New Label: {appeal_data['label']}")

        # 3. Rate Limit Verification (12 requests)
        log("\n[3/4] Testing Production Rate Limiting (10 req/min limit)")
        codes = []
        for i in range(12):
            resp = request_context.post("http://127.0.0.1:5000/submit", data={
                "text": "Rate limit test request.",
                "creator_id": "ratelimit-test"
            })
            codes.append(resp.status)

        log(f"-> Status codes for 12 rapid requests: {codes}")
        assert 429 in codes
        log("-> Verification: 429 Too Many Requests received as expected.")

        # 4. Dashboard Analytics Verification
        log("\n[4/4] Testing Analytics Dashboard")
        dash_resp = request_context.get("http://127.0.0.1:5000/dashboard", headers={
            "X-Admin-Key": "super-secret-admin-key",
            "Accept": "application/json"
        })
        assert dash_resp.status == 200
        stats = dash_resp.json()
        log(f"-> Dashboard Stats Received: {json.dumps(stats, indent=2)}")
        assert "appeal_rate" in stats
        assert "ai_to_human_ratio" in stats
        assert "average_confidence" in stats
        log("-> Verification: All calculated analytics fields present.")

        log("\n=====================================================")
        log("SYSTEM VERIFICATION SUCCESSFUL")

        # Save video path to a file for later summary
        actual_video_path = page.video.path()
        with open("video_path.txt", "w") as f:
            f.write(actual_video_path)

        time.sleep(2) # Finish video
        context.close()
        browser.close()

if __name__ == "__main__":
    pytest.main([__file__])
