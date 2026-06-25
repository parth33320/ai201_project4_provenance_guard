## What to build
Implement the second detection signal (Stylometrics) and the Weighted-Veto scoring engine.

## Acceptance criteria
- [ ] Stylometric signal measures TTR, variance, complexity, and punctuation.
- [ ] Scoring engine implements the "Human Defense Veto" logic.
- [ ] `POST /submit` includes both signals in the analysis.
- [ ] Audit log records individual signal scores.
- [ ] Confidence scores vary meaningfully between AI and Human test cases.

## Blocked by
- .scratch/provenance-guard/issues/01-tracer-bullet.md
