# ai201-project4-provenance-guard

Provenance Guard is a backend classification system designed for social writing platforms (e.g., Medium, Substack) to provide transparency about content origin while protecting human creators from false positives.

## Architecture

The system follows a multi-signal pipeline with a **Weighted-Veto Scoring Engine**.

1.  **Submission Flow**: `POST /submit` accepts text, runs it through LLM-based and Stylometric analysis, calculates a confidence score, and logs the result to a **SQLite** audit log.
2.  **Appeal Flow**: `POST /appeal` allows creators to contest labels. This updates the content status to `under_review` and changes the transparency label for readers.
3.  **Security**: The `/log` endpoint is protected by a simulated admin API key.
4.  **Resilience**: Rate limiting (10 requests per minute) prevents system abuse.

## Detection Signals

### 1. LLM-based Semantic Analysis (Groq Llama 3.3 70B)
- **Measures**: Linguistic patterns, structural rigidity, and semantic coherence common in AI output.
- **Strength**: High sensitivity to typical LLM instruction-following styles.
- **Blind Spot**: Can misclassify highly formal or academic human writing.

### 2. Stylometric Heuristics (Python)
- **Measures**: Sentence length variance, Type-Token Ratio (vocabulary diversity), Punctuation Density, and Average Sentence Complexity.
- **Strength**: Captures the inherent variability and "burstiness" of human thought.
- **Blind Spot**: Short or casual human writing can appear statistically uniform.

## Confidence Scoring: Weighted-Veto Model

The scoring engine prioritizes avoiding false positives (labeling humans as AI).
- **Logic**: If the Stylometric Human score is very high (>0.85), it "vetos" or significantly reduces any AI markers found by the LLM.
- **Validation**: Tested against formal academic writing (which LLMs often flag) to ensure the stylometric signal pulls the score back into the "Uncertain" or "Human" tier.

## Transparency Labels (Objective & Neutral)

| Variant | Exact Text |
| :--- | :--- |
| **High-Confidence Human** | "Human-Authored: This content displays the stylistic variability characteristic of human writing." |
| **Uncertain** | "Attribution Neutral: Our analysis found mixed signals regarding the origin of this content." |
| **High-Confidence AI** | "AI-Generated: This content matches patterns consistently associated with large language model output." |
| **Under Review** | "Humanity Verification in Progress (Under Review): A creator has contested the automated label." |

## Rate Limiting

- **Limit**: 10 requests per minute per IP.
- **Reasoning**: This accommodates typical human writing patterns (one post every few minutes) while blocking scripts or automated tools from flooding the attribution engine.

## Known Limitations

- **Short Text**: Submissions under 100 words provide insufficient data for stylometric signals, often leading to "Uncertain" classifications.
- **Highly Edited AI**: Lightly edited AI text can bypass stylometric checks while retaining enough semantic markers to be "Uncertain," which reflects genuine system ambiguity.

## Spec Reflection

- **Spec Alignment**: The implementation followed the vertical slices defined in `planning.md` precisely.
- **Divergence**: During implementation of the `ScoringEngine`, I moved the Veto threshold from 0.9 (initial design) to 0.85 after realizing that formal academic human writing was hovering around 0.8 on stylometrics, requiring a slightly lower threshold to trigger the "Human Defense."

## AI Usage

1.  **Skeleton Generation**: Used AI to generate the initial Flask app and SQLite table structure based on `ARCHITECTURE.md`. I revised the `audit_log` table to include `stylo_score` and `llm_score` separately for deeper transparency.
2.  **Scoring Logic**: Used AI to draft the stylometric metric functions. I overrode the weighting (increasing Sentence Length Variance to 40%) after testing revealed it was the most reliable differentiator for human "burstiness."

## Setup

1.  Install dependencies: `pip install -r requirements.txt`
2.  Initialize DB: `python init_db.py`
3.  Set `GROQ_API_KEY` in `.env`.
4.  Run app: `python app.py`
