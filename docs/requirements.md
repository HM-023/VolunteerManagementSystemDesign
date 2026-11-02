# Product requirements — fictional nonprofit

## Actors

- **Volunteer:** registers interest, sees open opportunities, updates availability.
- **Coordinator:** creates opportunities, reviews interests and assigns volunteers.
- **Donor:** expresses an offer to donate resources or goods.
- **Administrator:** maintains access controls and audits activity.

## Functional requirements (proposed, not fully implemented)

| ID | Requirement | Priority | Demo implementation |
|---|---|---|---|
| FR-01 | Enter volunteer name and area of interest | High | In-memory form only |
| FR-02 | Show a list of entered volunteers | High | In-memory grid only |
| FR-03 | Record a donation intent and category | High | In-memory form only |
| FR-04 | Create community opportunities | High | Not implemented |
| FR-05 | Match volunteers to opportunities | Medium | Not implemented |
| FR-06 | Role-based authentication | High | Not implemented |
| FR-07 | Review/approve resource requests | High | Not implemented |
| FR-08 | Audit data changes and export reports | High | Not implemented |

## Quality requirements

- **Privacy:** minimize personally identifiable data and provide retention/deletion policies.
- **Security:** authenticating users, access control, validation, encryption and audit records for production.
- **Accessibility:** keyboard navigation, readable contrast and text alternatives.
- **Reliability:** safe persistence, recoverable backups and transaction handling.
- **Maintainability:** separate UI, domain logic and storage layers for a production build.

## Important boundary

The public Windows Forms example uses fictitious/session-only data and does not satisfy most product requirements. It should not be deployed to accept real donations or store personal records.
