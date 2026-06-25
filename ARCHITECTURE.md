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

    C->>API: POST /submit (text, creator_id)
    API->>P: Analyze Text
    P->>P: Signal 1 (LLM Semantic)
    P->>P: Signal 2 (Stylometric Heuristic)
    P-->>API: Signal Scores
    API->>SE: Calculate Combined Score
    SE-->>API: Confidence Score & Label
    API->>DB: Log Submission & Results
    DB-->>API: content_id
    API-->>C: JSON (content_id, attribution, confidence, label)
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

## Deep Module: Scoring Engine

The `ScoringEngine` is a deep module that hides the complexity of multi-signal reconciliation.

- **Interface**: `calculate_score(signals: Dict[str, float]) -> Tuple[str, float, str]`
- **Implementation**: Implements the "Weighted-Veto" logic where high-confidence human signals can override AI-leaning signals to minimize false positives.

## Data Seams

- **API Seam**: The boundary between the Flask routes and the core logic.
- **Signal Seam**: The boundary between the pipeline and individual detection modules (LLM, Stylometrics).
- **Storage Seam**: The boundary between the application and the SQLite database.
