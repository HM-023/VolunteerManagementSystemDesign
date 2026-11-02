# Use cases

## UC-01 — Volunteer expresses interest

**Actor:** Volunteer. **Trigger:** Wants to participate. **Precondition:** Application is available.

1. Volunteer opens the interest form.
2. Volunteer provides a name or alias and an activity preference.
3. System validates required fields.
4. System displays the draft interest entry.

**Design future-state:** an authenticated flow would persist the record, support consent/retention choices, and notify a coordinator. The demo stops after step 4.

## UC-02 — Donor registers donation intent

**Actor:** Donor. **Trigger:** Wants to offer goods/resources.

1. Donor selects a category and enters a description.
2. System validates required fields.
3. System lists the intent for the current session.

**Design future-state:** route for review, assignment, and fulfillment, with no payment collection in the demo.

## UC-03 — Coordinator assigns volunteer (not implemented)

1. Coordinator reviews verified volunteer availability.
2. Coordinator selects a suitable opportunity.
3. System prevents incompatible/double-booked assignments.
4. Notifications and audit history are recorded.
