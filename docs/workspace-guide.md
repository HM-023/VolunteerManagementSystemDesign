# Volunteer Management System Design: workspace guide

## Start and stop

Use `python -m webapp.app` from the repository root and open the printed loopback address. Python 3.11 or later is the supported baseline. Use the virtual environment activation command for your operating system. The default port is 8105; `--port` changes it. `Ctrl+C` shuts down the server.

## Main workflow

1. Start with an empty workspace, or explicitly load fictional demo aliases from the overview. The app never seeds real personal information.
2. Add volunteers with an alias and comma-separated skills. Skills are trimmed, deduplicated and normalized to lowercase.
3. Create opportunities with a required skill, ISO calendar date and capacity of 1–1,000. Dates may describe historical or planned activities. This version schedules by day, not by time slot.
4. Assign a volunteer. The server checks that the skill matches, the opportunity has room and the volunteer has no assignment on the same date. Capacity and availability checks run inside an immediate SQLite transaction to prevent competing requests from overbooking a place.
5. Remove an assignment to release the place. Deleting a volunteer or opportunity also removes its related assignments. Activity records note local changes; the UI shows the latest 40 events.
6. Record a resource offer. A pledge can become received or withdrawn. A received intent can become distributed. Distributed and withdrawn are terminal states; the app rejects backwards or skipped transitions. This tracks goods/resource intents and does not collect money.
7. Export a snapshot if needed and review it before sharing. This is a single-user loopback tool; it has no identity provider, roles, remote access, email, consent management or payment processing. The previous C# prototype is retained separately.

## Local data and backups

Records live in `data/workspace.sqlite3` by default. ML model artifacts additionally live in `data/models/`. These paths are excluded from git. The file formats contain local workspace information and are not encrypted by the application. Stop the server before copying the entire data directory for a simple backup, then use `--data-dir` to reopen that copy. Deleting the data directory while the server is stopped resets the workspace. Exported files are saved wherever the browser downloads them; this app does not automatically publish them.

## Local browser boundary

Use the exact printed localhost/127.0.0.1 URL and reload after restarting the server. A new random session token is issued each time. There is no remote bind option. Host checks resist DNS rebinding, and API requests require the page's token. This is a browser-request boundary, not account authentication and not a defense against other software already running as the same operating-system user.

## Browser verification

GitHub Actions runs the end-to-end journey in `tests/browser.cjs` using pinned Playwright 1.56.1. It exercises real forms and local API actions, checks browser errors and mobile viewport fit, reloads persisted state and captures desktop/mobile PNGs. Screenshots use only synthetic or fictional inputs.
