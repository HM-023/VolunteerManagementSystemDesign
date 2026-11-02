# Acceptance criteria and test status

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| A-01 | Leave volunteer name blank | UI shows a validation warning | Implemented, Windows run not verified |
| A-02 | Provide a name and activity | New row appears in session list | Implemented, Windows run not verified |
| A-03 | Leave donation description blank | UI shows a validation warning | Implemented, Windows run not verified |
| A-04 | Add a donation intent | New row appears in session list | Implemented, Windows run not verified |
| A-05 | Restart application | Session data is reset | By design, no persistence |
| A-06 | User logs in with a role | Authorization is enforced | Not implemented |
| A-07 | Multiple users edit concurrently | Conflicts handled safely | Not implemented |

The .NET SDK was unavailable in the local review environment, so compilation and GUI testing were not executed. A Windows GitHub Actions build workflow is included but has not run for this publication yet. Complete manual acceptance testing on Windows before describing the UI as verified.
