# Architecture: Provenance Guard

Provenance Guard is designed as a deep classification system for content attribution. It prioritizes avoiding false positives through a multi-signal pipeline and a Weighted-Veto scoring engine.

## Submission Flow

The submission flow transforms raw text into a classified content entry with a transparency label and a confidence score.

```mermaid
sequenceDiagram
    participant C as Creator
    participant API as Flask API (/submit)
    participant P as Detection Pipeline
    participant SE as Scoring Engine (Weighted-Veto)
    participant DB as SQLite (Audit Log)

    C->>API: POST /submit (text, content_type, creator_id)
    API->>DB: Check Creator Verification Status
    alt Content Type is Text
        API->>P: Analyze Text
        P->>P: Signal 1 (LLM Semantic)
        P->>P: Signal 2 (Stylometric Heuristic)
    else Content Type is Image Description
        API->>P: Analyze Alt-text
        P->>P: Signal 3 (LLM Semantic)
        P->>P: Signal 4 (Template Conformity)
        P->>P: Signal 5 (Descriptive Verbosity)
    end
    P-->>API: Signal Scores
    API->>SE: Calculate Combined Score
    SE-->>API: Confidence Score & Label
    API->>DB: Log Submission & Results (including is_verified snapshot)
    DB-->>API: content_id
    API-->>C: JSON (content_id, attribution, confidence, label, provenance_certificate)
```

## Appeal Flow

The appeal flow allows creators to contest classifications, updating the state and providing an audit trail for review.

```mermaid
sequenceDiagram
    participant C as Creator
    participant API as Flask API (/appeal)
    participant DB as SQLite (Audit Log)

    C->>API: POST /appeal (content_id, reasoning)
    API->>DB: Update Status to 'Under Review'
    API->>DB: Log Appeal Reasoning
    DB-->>API: Success
    API-->>C: JSON (Status: Under Review)
```

## Verification Flow

The verification flow allows a creator to earn a 'Verified Provenance' status through a one-time identity verification.

```mermaid
sequenceDiagram
    participant C as Creator
    participant API as Flask API (/verify)
    participant DB as SQLite (Verified Creators)

    C->>API: POST /verify (creator_id, token)
    API->>API: Validate Token
    API->>DB: Store Verified Status
    DB-->>API: Success
    API-->>C: JSON (Status: Verified)
```

## JSON Schema: Provenance Certificate

The `Provenance Certificate` is included in the `/submit` response as metadata.

```json
{
  "type": "object",
  "properties": {
    "content_id": { "type": "string" },
    "attribution": { "type": "string" },
    "confidence": { "type": "number" },
    "label": { "type": "string" },
    "provenance_certificate": { "type": "boolean" }
  },
  "required": ["content_id", "attribution", "confidence", "label", "provenance_certificate"]
}
```

## Deep Module: Scoring Engine

The `ScoringEngine` is a deep module that hides the complexity of multi-signal ensemble reconciliation and routing.

- **Interface**: `calculate_weighted_veto_score(llm_ai_score, stylo_human_score, burst_score, content_type, multimodal_scores)`
- **Implementation**: Implements the "Human Defense Veto" logic where high-confidence human markers (Stylometric variability or Paragraph Burstiness) can override AI markers to prevent false positives for human creators. It reduces the final AI confidence score and caps it at 0.3 (Likely Human tier) if human markers exceed a 0.85 threshold.

## Data Seams

- **API Seam**: The boundary between the Flask routes and the core logic.
- **Signal Seam**: The boundary between the pipeline and individual detection modules (LLM, Stylometrics).
- **Storage Seam**: The boundary between the application and the SQLite database.
