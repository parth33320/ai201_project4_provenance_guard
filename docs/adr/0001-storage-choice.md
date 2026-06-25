# 0001: Storage Choice for Audit Logs and Appeals

## Context
The system requires a persistent, structured storage mechanism to record every attribution decision (Audit Log) and track the status of creator appeals. The requirements include durability, structured querying (for the `/log` endpoint and appeal status updates), and a "production-first" mindset.

## Decision
We will use **SQLite** as the primary storage engine.

## Rationale
- **Structured Data**: SQLite allows us to define a clear schema for logs and appeals, ensuring data consistency.
- **Queryability**: It enables efficient filtering and retrieval of log entries for the administrative dashboard.
- **Durability**: Unlike flat JSON files, SQLite provides ACID properties, ensuring that logs are not lost or corrupted during concurrent writes.
- **Zero-Config**: It is serverless and requires no additional infrastructure setup, making it ideal for the project's scope while maintaining professional standards.
- **Relational Integrity**: Appeals can be easily linked to their original submission entries using foreign keys.

## Consequences
- We will need to manage a database schema and handle connections within the Flask application.
- We must ensure the database file is included in `.gitignore` if it contains sensitive test data, though for this project, the log itself is a primary deliverable.
