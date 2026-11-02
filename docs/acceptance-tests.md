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

The .NET SDK was unavailable in the local review environment. The [hosted Windows build](https://github.com/HM-023/VolunteerManagementSystemDesign/actions/runs/41430901903) passed on 2026-11-02 using the .NET 8 SDK. Compilation is verified; interactive GUI behavior and the manual acceptance scenarios above remain unverified.
