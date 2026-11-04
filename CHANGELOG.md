# Changelog

## 1.0.0 — Local workspace release (2026-11-04)

- Volunteer directory: Store aliases and normalized skills in SQLite.
- Opportunity planning: Create activities with a required skill, date and capacity.
- Transactional matching: Require matching skills, prevent capacity overbooking and reject same-day assignment conflicts.
- Resource intents: Track pledged goods through received and distributed states, or withdraw an unreceived pledge.
- Activity history: Record local additions, assignments, resource transitions and removals.
- Persistence and export: Reload saved records after restart and export a local JSON snapshot.
- Added a responsive local dashboard, request-boundary validation, ignored local state, regression tests and browser workflow verification.
- Preserved the prior case-study material and its contribution/reuse limitations.

Remaining scope: The new Python web app is a single-user local tool with SQLite persistence. It does not provide authentication, role-based access, notifications, payment processing or hosted multi-user operation. The earlier C# Windows Forms prototype remains in prototype/ as a separate, session-only UI example.
