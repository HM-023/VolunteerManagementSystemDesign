![Volunteer Management System Design](assets/cover.svg)

# Volunteer Management System Design

**Persistent local community operations app** · [User guide](docs/workspace-guide.md) · [Architecture](docs/workspace-architecture.md) · [Verification](docs/workspace-verification.md) · [Portfolio](https://github.com/HM-023)

[![Workspace verification](https://github.com/HM-023/VolunteerManagementSystemDesign/actions/workflows/workspace.yml/badge.svg)](https://github.com/HM-023/VolunteerManagementSystemDesign/actions/workflows/workspace.yml)

Store aliases and normalized skills in SQLite. The repository now includes a working, browser-based local workspace with a responsive dashboard and persistent records.

## What you can do

| Capability | Working behavior |
|:---|:---|
| **Volunteer directory** | Store aliases and normalized skills in SQLite. |
| **Opportunity planning** | Create activities with a required skill, date and capacity. |
| **Transactional matching** | Require matching skills, prevent capacity overbooking and reject same-day assignment conflicts. |
| **Resource intents** | Track pledged goods through received and distributed states, or withdraw an unreceived pledge. |
| **Activity history** | Record local additions, assignments, resource transitions and removals. |
| **Persistence and export** | Reload saved records after restart and export a local JSON snapshot. |

## Run locally

Requires **Python 3.11+**. Run commands from this repository's root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m webapp.app
```

Open **http://127.0.0.1:8105** in your browser. Stop the server with `Ctrl+C`.

Four workspaces use only Python's standard library. The ML workspace uses the packages in `requirements.txt`. The browser UI loads no external fonts, scripts, analytics or services. After dependencies are installed, the applications run offline.

For a different local port or data directory:

```bash
python -m webapp.app --port 8205 --data-dir path/to/local-workspace
```

## Architecture

![Local workspace architecture](assets/architecture.svg)

The server binds to loopback, checks the Host header and requires a fresh per-process token for API access. Mutations also reject foreign browser origins. Local data lives under `data/` by default; database files, model files and generated outputs are excluded from version control.

## Verify the implementation

```bash
python -m unittest discover -s tests -v
```

The [workspace workflow](https://github.com/HM-023/VolunteerManagementSystemDesign/actions/workflows/workspace.yml) runs domain tests and an automated browser journey on GitHub. Browser runs upload real desktop and mobile captures as the **workspace-screenshots** artifact. See the verification document for the exact tested boundaries.

## Implementation boundaries

The new Python web app is a single-user local tool with SQLite persistence. It does not provide authentication, role-based access, notifications, payment processing or hosted multi-user operation. The earlier C# Windows Forms prototype remains in prototype/ as a separate, session-only UI example.

These are local portfolio applications, with documented scope and tested workflows. They are not deployed enterprise services. No synthetic model score is presented as a real-world detection benchmark, and no generated network diagram or policy decision is presented as live network evidence.

## Repository map

| Path | Purpose |
|:---|:---|
| `webapp/app.py` | Application actions and local workspace state |
| `webapp/runtime.py` | Loopback HTTP boundary and SQLite document storage |
| `webapp/static/` | Responsive dashboard, forms, tables, charts and exports |
| `tests/` | Domain, persistence, server-boundary and browser checks |
| `docs/workspace-guide.md` | Usage, input formats and local-data operations |
| `docs/reference-case-study.md` | Prior case study, historical context and attribution |

## Provenance and reuse

The workspace code and generic examples are newly authored. Historical collaborative source materials, private datasets, credentials and organization-specific documents remain excluded. The [reference case study](docs/reference-case-study.md), [publication notes](PUBLICATION_NOTES.md) and existing security guidance retain the original contribution and reuse boundaries. No blanket license has been added to historical material.
