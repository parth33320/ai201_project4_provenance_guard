# 0002-provenance-certificate

To implement the Provenance Certificate stretch goal, we will introduce a verified creator status that adds a high-trust metadata layer to content submissions.

## Context
The system needs to distinguish between standard human-authored content and content from creators who have undergone a one-time verification step. This builds trust and provides an additional credential beyond automated detection signals.

## Decision
1.  **Persistence**: We will use a separate `verified_creators` table in SQLite to store the persistent status of verified creators.
2.  **Snapshotting**: At the time of submission, the verification status of the creator will be snapshotted into the `audit_log` table (column: `is_verified`). This ensures historical accountability even if a creator's status is later revoked.
3.  **Verification API**: A new `POST /verify` endpoint will be implemented, requiring a `creator_id` and a secret token to mimic a secure verification process.
4.  **Labeling**: Verified creators will have a "Verified Provenance: " prefix added to their transparency labels.
5.  **Scoring**: The verification status will have no impact on the raw AI/Human confidence scores to maintain the objectivity of the detection pipeline.
6.  **Response**: The `/submit` endpoint will include a `provenance_certificate` boolean in its JSON response.

## Consequences
- Readers gain immediate clarity on content origin from verified sources.
- The system remains robust against false positives by layering trust without compromising detection signals.
- Historical submissions maintain their verified status in the audit log regardless of subsequent status changes for the creator.
