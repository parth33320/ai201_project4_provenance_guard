import sqlite3

def get_analytics_summary(db_path='provenance_guard.db'):
    """
    Deep Module: Encapsulates complex data aggregation logic for the dashboard.
    Returns a dictionary of metrics for the UI.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    stats = conn.execute('''
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN attribution = 'likely_ai' THEN 1 ELSE 0 END) as ai_count,
            SUM(CASE WHEN attribution = 'likely_human' THEN 1 ELSE 0 END) as human_count,
            SUM(CASE WHEN attribution = 'uncertain' THEN 1 ELSE 0 END) as uncertain_count,
            SUM(CASE WHEN status = 'under_review' THEN 1 ELSE 0 END) as appeal_count,
            SUM(CASE WHEN is_verified = 1 THEN 1 ELSE 0 END) as verified_count,
            AVG(confidence) as average_confidence
        FROM audit_log
    ''').fetchone()
    conn.close()

    data = dict(stats)
    total = data['total'] or 0
    ai_count = data['ai_count'] or 0
    human_count = data['human_count'] or 0
    appeal_count = data['appeal_count'] or 0

    # Calculated Analytics (Deep Module behavior)
    data['appeal_rate'] = round(appeal_count / total, 4) if total > 0 else 0
    data['ai_to_human_ratio'] = round(ai_count / human_count, 2) if human_count > 0 else (ai_count if ai_count > 0 else 0)
    data['average_confidence'] = round(data['average_confidence'] or 0, 2)

    # Calculate AI vs Human Ratio as percentage for UI
    data['ai_percentage'] = round((ai_count / total) * 100, 1) if total > 0 else 0
    data['human_percentage'] = round((human_count / total) * 100, 1) if total > 0 else 0
    data['uncertain_percentage'] = round((data['uncertain_count'] / total) * 100, 1) if total > 0 else 0

    return data
