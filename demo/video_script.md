# Provenance Guard: Demo Video Script

## Scene 1: Architectural Foundations (0:00 - 0:30)
**Visuals:** Scrolling through ARCHITECTURE.md, CONTEXT.md, and planning.md.
**Narration:**
Welcome to Provenance Guard, a backend classification engine designed to protect content attribution. We began by defining our Ubiquitous Language in CONTEXT.md, establishing clear boundaries between attribution and detection. Our ARCHITECTURE.md outlines a multi-signal pipeline that prioritizes avoiding false positives through a Weighted-Veto scoring engine. Every design decision, from storage seams to API contracts, was documented in our planning.md before a single line of code was written.

## Scene 2: Multi-Signal Submission (0:30 - 1:00)
**Visuals:** POST /submit with 'Ramen Review' text, showing structured JSON response.
**Narration:**
Let's see the system in action. We submit a casual Ramen Review. The backend processes this through our multi-signal pipeline, including LLM semantic analysis and stylometric heuristics. The response is a structured JSON object containing a unique content ID, a confidence score, and a transparency label. Here, the high variability in sentence length and vocabulary produces a high human confidence score, resulting in a clear 'Human-Authored' label.

## Scene 3: The Human Defense Veto (1:00 - 1:30)
**Visuals:** POST /submit with 'Monetary Policy' text. Overlay: "Human Defense Veto Triggered".
**Narration:**
Provenance Guard excels at handling formal human writing which often confuses basic detectors. Submitting this 'Monetary Policy' text initially triggers AI-leaning semantic markers in the LLM. However, our Weighted-Veto logic detects strong human stylometric signals above our zero-point-eight-five threshold. This triggers a 'Human Defense Veto', capping the AI confidence at zero-point-three and protecting the human creator from a false classification.

## Scene 4: Navigating Uncertainty (1:30 - 2:00)
**Visuals:** POST /submit with 'Edited AI' text. Overlay: "Attribution Neutral Label".
**Narration:**
Absolute certainty isn't always possible, especially with edited AI content. When we submit this hybrid text, the signals return conflicting data. Instead of forcing a binary choice, Provenance Guard honestly communicates uncertainty. The resulting confidence score falls into our middle-tier range, triggering the 'Attribution Neutral' transparency label. This provides readers with the context they need without making definitive, unverified claims.

## Scene 5: Appeals and Transparency (2:00 - 2:30)
**Visuals:** POST /appeal followed by GET /log showing the audit log.
**Narration:**
Transparency requires accountability. If a creator believes a classification is incorrect, they can submit an appeal. By sending a POST request to the appeal endpoint with their reasoning, the system updates the content's status in our SQLite audit log. As we view the log, we see the entry transition to 'under review'. This append-only audit trail ensures that every classification and contestation is recorded for human oversight.

## Scene 6: Production Safety and Analytics (2:30 - 3:00)
**Visuals:** A loop of 12 requests hitting a 429 error, followed by /dashboard JSON. Overlay: "429 Rate Limit Hit".
**Narration:**
Finally, we ensure production stability with rate limiting and analytics. Attempting to flood the submission endpoint triggers a four-two-nine Too Many Requests error after our limit is reached. For administrators, the dashboard endpoint provides a high-level view of system health, including the AI-to-human ratio, appeal rates, and average confidence scores across all submissions. This is Provenance Guard: precise, transparent, and built for trust.
