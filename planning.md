# Planning: Provenance Guard

## Detection Signals

### Signal 1: LLM-based Semantic Analysis (Groq)
- **What it measures**: Semantic coherence, typical AI linguistic patterns (over-structured transitions, neutral/clinical tone, lack of personal anecdote).
- **Output**: A score from 0.0 (Likely Human) to 1.0 (Likely AI).
- **Blind spot**: Highly formal or academic human writing can be mistaken for AI.

### Signal 2: Stylometric Heuristics (Python)
- **What it measures**: Sentence length variance, Type-Token Ratio (vocabulary diversity), Punctuation Density, and Average Sentence Complexity.
- **Output**: A score from 0.0 (Likely AI/Uniform) to 1.0 (Likely Human/Variable).
- **Blind spot**: Simple human writing (e.g., social media posts) can appear "uniform" and trigger false AI positives.

### Signal Combination (Weighted-Veto)
- The system will use the **Human Defense Veto** logic. A high Stylometric Human score (>0.85) will significantly down-weight or override an AI-leaning LLM score to protect human creators.

## Uncertainty Representation

We define three confidence tiers based on the combined score (0.0 to 1.0, where 1.0 is AI):

- **High-Confidence Human (0.0 - 0.3)**: Low AI markers, high structural variability.
- **Uncertain (0.31 - 0.7)**: Conflicting signals or mid-range markers.
- **High-Confidence AI (0.71 - 1.0)**: High AI markers, low structural variability.

## Transparency Label Design (Objective & Neutral)

| Tier | Label Text |
| :--- | :--- |
| **High-Confidence Human** | "Human-Authored: This content displays the stylistic variability characteristic of human writing." |
| **Uncertain** | "Attribution Neutral: Our analysis found mixed signals regarding the origin of this content." |
| **High-Confidence AI** | "AI-Generated: This content matches patterns consistently associated with large language model output." |
| **Under Review** | "Humanity Verification in Progress (Under Review): A creator has contested the automated label." |

## Appeals Workflow
1. **Endpoint**: `POST /appeal`
2. **Input**: `content_id`, `creator_reasoning`.
3. **Action**:
   - Update `status` to `under_review` in SQLite.
   - Update `transparency_label` to the "Under Review" variant.
   - Log the reasoning in the `audit_log` table.
4. **Visibility**: Admin can view appeals via `GET /log`.

## Anticipated Edge Cases
1. **Academic/Legal Writing**: Formal human writing often has low TTR and uniform sentence lengths, potentially triggering a false AI positive.
2. **Very Short Text**: Below 100 words, stylometric signals are unreliable due to small sample size. The system should default to "Uncertain" if signals are too weak.

## AI Tool Plan

### Milestone 1: Tracer Bullet
- **Input**: `planning.md` + `ARCHITECTURE.md`
- **Request**: Generate Flask app with SQLite schema and `POST /submit` using Groq signal only.
- **Verification**: Playwright test calling `/submit` and checking SQLite log.

### Milestone 2: Multi-Signal & Scoring
- **Input**: `planning.md` + Scoring Engine design.
- **Request**: Implement Stylometric signal and Weighted-Veto logic.
- **Verification**: Test 4 inputs (AI, Human, Formal Human, Social Human) to verify score variance.

### Milestone 3: Production Layer
- **Input**: `planning.md` + Appeals Workflow.
- **Request**: Implement `/appeal`, rate limiting, and admin-protected `/log`.
- **Verification**: Trigger 429 response via rapid requests; Verify appeal reasoning appears in log.
