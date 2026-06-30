import sqlite3
import uuid
import datetime

DB_PATH = 'provenance_guard.db'

def seed_data():
    conn = sqlite3.connect(DB_PATH)

    # Clear existing log for clean test
    conn.execute('DELETE FROM audit_log')

    entries = [
        # 1. AI-Generated (high confidence)
        {
            "content_id": str(uuid.uuid4()),
            "creator_id": "creator_ai_1",
            "text": "The industrial revolution and its consequences have been a disaster for the human race. It has greatly increased the life-expectancy of those of us who live in 'advanced' countries, but it has destabilized society, has made life unfulfilling, has subjected human beings to indignities, has led to widespread psychological suffering.",
            "content_type": "text",
            "attribution": "likely_ai",
            "confidence": 0.92,
            "llm_score": 0.95,
            "stylo_score": 0.1,
            "status": "classified",
            "is_verified": 0
        },
        # 2. Human-Authored (high confidence)
        {
            "content_id": str(uuid.uuid4()),
            "creator_id": "creator_human_1",
            "text": "Wait, did I leave the stove on? I was thinking about the way the light hits the trees in October... you know, that golden, dusty quality that makes everything look like a memory even while it's happening? Anyway, I should probably check the kitchen. Or just keep writing. The writing feels more important than the possibility of fire right now, strangely enough.",
            "content_type": "text",
            "attribution": "likely_human",
            "confidence": 0.15,
            "llm_score": 0.2,
            "stylo_score": 0.9,
            "status": "classified",
            "is_verified": 1
        },
        # 3. Attribution Neutral (uncertain)
        {
            "content_id": str(uuid.uuid4()),
            "creator_id": "creator_neutral_1",
            "text": "This is a relatively standard piece of technical documentation regarding the implementation of the new API endpoints. It covers the basic requirements and provides some examples of the expected response formats.",
            "content_type": "text",
            "attribution": "uncertain",
            "confidence": 0.5,
            "llm_score": 0.6,
            "stylo_score": 0.5,
            "status": "classified",
            "is_verified": 0
        },
        # 4. Under Review (contested appeal)
        {
            "content_id": str(uuid.uuid4()),
            "creator_id": "creator_appeal_1",
            "text": "I am deeply offended that my personal memoir was flagged as AI. This story is about my grandmother and the specific dialect she used in the Appalachians. No AI could replicate the soul I put into this.",
            "content_type": "text",
            "attribution": "likely_ai", # Originally AI, now appealed
            "confidence": 0.75,
            "llm_score": 0.8,
            "stylo_score": 0.3,
            "status": "under_review",
            "appeal_reasoning": "This is a personal memoir with specific cultural nuances.",
            "is_verified": 0
        },
        # 5. Verified AI (Mixed signal but verified creator)
        {
            "content_id": str(uuid.uuid4()),
            "creator_id": "creator_verified_ai",
            "text": "The quick brown fox jumps over the lazy dog. A common pangram used to test typewriters and computer keyboards. It contains every letter of the English alphabet.",
            "content_type": "text",
            "attribution": "likely_ai",
            "confidence": 0.85,
            "llm_score": 0.9,
            "stylo_score": 0.2,
            "status": "classified",
            "is_verified": 1
        }
    ]

    for entry in entries:
        conn.execute('''
            INSERT INTO audit_log (
                content_id, creator_id, text, content_type, attribution, confidence,
                llm_score, stylo_score, status, appeal_reasoning, is_verified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry['content_id'], entry['creator_id'], entry['text'], entry['content_type'],
            entry['attribution'], entry['confidence'], entry['llm_score'], entry['stylo_score'],
            entry['status'], entry.get('appeal_reasoning'), entry['is_verified']
        ))

    conn.commit()
    conn.close()
    print("Seeded 5 diverse entries into audit_log.")

if __name__ == "__main__":
    seed_data()
