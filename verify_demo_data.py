import os
import requests
import json
import time
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Specific texts from Milestone 4 hints
RAMEN_REVIEW = "ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably won't go back unless someone drags me there"

MONETARY_POLICY = "The relationship between monetary policy and asset price inflation has been extensively studied in the literature. Central banks face a fundamental tension between their mandate for price stability and the unintended consequences of prolonged low interest rates on equity and real estate valuations."

EDITED_AI = "I've been thinking a lot about remote work lately. There are genuine tradeoffs — flexibility and no commute on one side, isolation and blurred work-life boundaries on the other. Studies show productivity varies widely by individual and role type."

AI_GEN = "Artificial intelligence represents a transformative paradigm shift in modern society. It is important to note that while the benefits of AI are numerous, it is equally essential to consider the ethical implications. Furthermore, stakeholders across various sectors must collaborate to ensure responsible deployment."

def verify():
    # Start server
    print("Starting server...")
    server = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5) # Wait for server to start

    try:
        samples = [
            ("Ramen Review", RAMEN_REVIEW),
            ("Monetary Policy", MONETARY_POLICY),
            ("Edited AI", EDITED_AI),
            ("AI Generated", AI_GEN)
        ]

        for name, text in samples:
            print(f"\nTesting: {name}")
            try:
                response = requests.post("http://localhost:5000/submit", json={
                    "text": text,
                    "creator_id": "test_user"
                })
                print(json.dumps(response.json(), indent=2))
            except Exception as e:
                print(f"Request failed: {e}")

    finally:
        print("\nStopping server...")
        server.terminate()
        server.wait()

if __name__ == "__main__":
    verify()
