import asyncio
import os
import subprocess
import time
import json
import shutil
from playwright.async_api import async_playwright

# Specific texts from Milestone 4 hints
RAMEN_REVIEW = "ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably won't go back unless someone drags me there"
MONETARY_POLICY = "The relationship between monetary policy and asset price inflation has been extensively studied in the literature. Central banks face a fundamental tension between their mandate for price stability and the unintended consequences of prolonged low interest rates on equity and real estate valuations."
EDITED_AI = "I've been thinking a lot about remote work lately. There are genuine tradeoffs — flexibility and no commute on one side, isolation and blurred work-life boundaries on the other. Studies show productivity varies widely by individual and role type."

async def record_scene(browser, url_or_action, scene_num, name):
    print(f"Recording Scene {scene_num}: {name}")
    video_dir = f"demo/clips/scene{scene_num}"
    os.makedirs(video_dir, exist_ok=True)

    context = await browser.new_context(
        record_video_dir=video_dir,
        record_video_size={"width": 1280, "height": 720},
        viewport={"width": 1280, "height": 720}
    )
    page = await context.new_page()

    if isinstance(url_or_action, str):
        # It's a file path or URL
        if url_or_action.startswith("http"):
            await page.goto(url_or_action)
        else:
            # For local files
            content = open(url_or_action).read()
            await page.goto("about:blank")
            await page.evaluate("(args) => { document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#cccccc'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px'; document.body.style.whiteSpace = 'pre-wrap'; document.body.innerHTML = '<h1>' + args.f + '</h1>' + args.c; }", {"f": url_or_action, "c": content})
            await asyncio.sleep(5)
    else:
        # It's a callback
        await url_or_action(page)

    await asyncio.sleep(2)
    await context.close()

    video_file = await page.video.path()
    target_path = f"demo/clips/scene{scene_num}.webm"
    if os.path.exists(target_path):
        os.remove(target_path)
    os.rename(video_file, target_path)
    shutil.rmtree(video_dir)

async def main():
    print("Initializing database...")
    subprocess.run(["python", "init_db.py"])

    print("Starting server...")
    server = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)

    print("Seeding data...")
    import requests
    texts = [RAMEN_REVIEW, MONETARY_POLICY, EDITED_AI, "Another human text example with high variability.", "This is a formal report on the state of the economy."]
    for i, t in enumerate(texts):
        requests.post("http://localhost:5000/submit", json={"text": t, "creator_id": f"user{i}"})

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Scene 1: ARCHITECTURE.md and CONTEXT.md
            async def scene1_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#cccccc'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                for filename in ["ARCHITECTURE.md", "CONTEXT.md", "planning.md"]:
                    content = open(filename).read()
                    await page.evaluate("(args) => { document.body.innerHTML += '<h1>' + args.f + '</h1><pre>' + args.c + '</pre><hr>'; }", {"f": filename, "c": content})
                    await asyncio.sleep(5)
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            await record_scene(browser, scene1_action, 1, "Architecture and Context")

            # Scene 2: Ramen Review
            async def scene2_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#00ff00'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                await page.evaluate("document.body.innerHTML = '<h1>POST /submit</h1><pre>Sending Ramen Review...</pre>'")
                await asyncio.sleep(2)
                import requests
                resp = requests.post("http://localhost:5000/submit", json={"text": RAMEN_REVIEW, "creator_id": "user1"})
                res_json = json.dumps(resp.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Response:</h2><pre>' + res + '</pre>'; }", res_json)
                await asyncio.sleep(5)

            await record_scene(browser, scene2_action, 2, "Ramen Review Submission")

            # Scene 3: Monetary Policy (Veto)
            async def scene3_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#00ff00'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                await page.evaluate("document.body.innerHTML = '<h1>POST /submit</h1><pre>Sending Monetary Policy (Formal Human Writing)...</pre>'")
                await asyncio.sleep(2)
                import requests
                resp = requests.post("http://localhost:5000/submit", json={"text": MONETARY_POLICY, "creator_id": "user1"})
                res_json = json.dumps(resp.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Response:</h2><pre>' + res + '</pre>'; }", res_json)
                await asyncio.sleep(5)

            await record_scene(browser, scene3_action, 3, "Monetary Policy (Veto Logic)")

            # Scene 4: Edited AI (Neutral)
            async def scene4_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#00ff00'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                await page.evaluate("document.body.innerHTML = '<h1>POST /submit</h1><pre>Sending Edited AI Content...</pre>'")
                await asyncio.sleep(2)
                import requests
                resp = requests.post("http://localhost:5000/submit", json={"text": EDITED_AI, "creator_id": "user1"})
                res_json = json.dumps(resp.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Response:</h2><pre>' + res + '</pre>'; }", res_json)
                await asyncio.sleep(5)

            await record_scene(browser, scene4_action, 4, "Edited AI (Neutral Label)")

            # Scene 5: Appeal and Log
            async def scene5_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#00ff00'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                import requests
                resp_sub = requests.post("http://localhost:5000/submit", json={"text": RAMEN_REVIEW, "creator_id": "user1"})
                content_id = resp_sub.json()['content_id']
                await page.evaluate("(cid) => { document.body.innerHTML = '<h1>POST /appeal</h1><pre>Appealing content_id: ' + cid + '...</pre>'; }", content_id)
                await asyncio.sleep(2)
                resp_app = requests.post("http://localhost:5000/appeal", json={"content_id": content_id, "creator_reasoning": "I wrote this myself."})
                res_app = json.dumps(resp_app.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Appeal Response:</h2><pre>' + res + '</pre>'; }", res_app)
                await asyncio.sleep(3)
                await page.evaluate("document.body.innerHTML += '<h1>GET /log</h1>'")
                resp_log = requests.get("http://localhost:5000/log", headers={"X-Admin-Key": "super-secret-admin-key"})
                res_log = json.dumps(resp_log.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Audit Log:</h2><pre>' + res + '</pre>'; }", res_log)
                await asyncio.sleep(2)
                # Scrolling to reveal more entries
                await page.mouse.wheel(0, 500)
                await asyncio.sleep(3)

            await record_scene(browser, scene5_action, 5, "Appeals Workflow")

            # Scene 6: Rate Limit and Dashboard
            async def scene6_action(page):
                await page.goto("about:blank")
                await page.evaluate("document.body.style.backgroundColor = '#1e1e1e'; document.body.style.color = '#00ff00'; document.body.style.fontFamily = 'monospace'; document.body.style.padding = '40px';")
                await page.evaluate("document.body.innerHTML = '<h1>Rate Limit Test (12 requests)</h1>'")
                import requests
                for i in range(12):
                    resp = requests.post("http://localhost:5000/submit", json={"text": "test", "creator_id": "test"})
                    await page.evaluate("(args) => { document.body.innerHTML += '<p>Request ' + (args.i+1) + ': Status ' + args.s + '</p>'; }", {"i": i, "s": resp.status_code})
                    if resp.status_code == 429:
                        await page.evaluate("document.body.innerHTML += '<p style=\"color:red\">429 RATE LIMIT HIT!</p>'")
                    await asyncio.sleep(0.5)
                await asyncio.sleep(2)
                await page.evaluate("document.body.innerHTML += '<h1>GET /dashboard</h1>'")
                resp_dash = requests.get("http://localhost:5000/dashboard", headers={"X-Admin-Key": "super-secret-admin-key"})
                res_dash = json.dumps(resp_dash.json(), indent=2)
                await page.evaluate("(res) => { document.body.innerHTML += '<h2>Dashboard Metrics:</h2><pre>' + res + '</pre>'; }", res_dash)
                await asyncio.sleep(2)
                # Scrolling to reveal more metrics
                await page.mouse.wheel(0, 500)
                await asyncio.sleep(3)

            await record_scene(browser, scene6_action, 6, "Rate Limiting and Dashboard")
            await browser.close()
    finally:
        server.terminate()
        server.wait()

if __name__ == "__main__":
    asyncio.run(main())
