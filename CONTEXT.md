# Provenance Guard Context

This system is a backend classification engine for a **Social Writing App** (e.g., Medium/Substack). Its purpose is to build trust through content transparency and attribution.

## Language

**Provenance Guard**:
The backend system responsible for classifying content origin and managing the attribution lifecycle.

**Attribution**:
The result of analyzing content to determine if it was human-written or AI-generated.
_Avoid_: Detection, Policing

**Detection Signal**:
An independent metric or analysis path used to evaluate content. Examples include LLM-based semantic analysis and stylometric heuristic analysis.
_Avoid_: Tool, Classifier

**Confidence Score**:
A value between 0.0 and 1.0 representing the system's certainty in an attribution result.
_Avoid_: Logit, Probability

**Transparency Label**:
The objective, neutral text surfaced to readers to provide context about a submission's origin.
_Avoid_: Verdict, Classification Label

**Appeal**:
A mechanism for creators to contest an attribution result by providing reasoning for human review.
_Avoid_: Dispute, Complaint

**Audit Log**:
A structured, append-only record of all submissions, scores, signals, and appeal events.

**Weighted-Veto Model**:
A scoring strategy designed to prioritize avoiding false positives (labeling human work as AI) by allowing high-confidence human signals to override AI signals.

**Verified Creator**:
A creator who has undergone a one-time identity verification process. Their status is recorded in a persistent registry.

**Provenance Certificate**:
A high-trust metadata layer added to a submission from a **Verified Creator**, providing an additional layer of trust beyond automated analysis.

**Image Description (Alt-text)**:
A short text alternative for images. This is a second content type supported by the system for multi-modal transparency.

**Template Conformity**:
A detection signal for Image Descriptions that identifies formulaic patterns typical of AI-generated descriptions (e.g., "A photo of...").

**Descriptive Verbosity**:
A detection signal for Image Descriptions that measures the clinical and overly detailed nature of the text compared to subjective human writing.

## Relationships

- A **Submission** is analyzed by multiple **Detection Signals**.
- **Detection Signals** are combined by the **Scoring Engine** to produce a **Confidence Score**.
- The **Confidence Score** determines which **Transparency Label** is displayed.
- A **Creator** can file an **Appeal** against a **Submission**'s attribution.
- A **Verified Creator** receives a **Provenance Certificate** for all their **Submissions**.
- All actions are recorded in the **Audit Log**.
