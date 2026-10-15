# EMS1-6201 dashboardAlarmAckClearLog

## Purpose

Verify that acknowledging and clearing an active alarm from the Dashboard creates the corresponding successful Access Log records with the same alarm ID and sub-ID.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, and password

## Preconditions

- Dashboard Alarm Status contains at least one active alarm.
- The first active alarm can be acknowledged and cleared.
- The login account can access `System/Security/Access Log`.

## Steps

1. Login to EMS Web and open `Dashboard`.
2. If the total Alarm Status count is zero, mark the case as skipped.
3. Select the total Alarm Status and click the `more...` link.
4. Switch to the newly opened Active Alarm window.
5. Select the first row and remember its `index_1` and `index_2` attributes.
6. Record the Ack operation time and click the Ack icon.
7. Verify the success message and click `OK`.
8. Find the same row by `index_1` and `index_2`, then select it.
9. Record the Clear operation time and click the Clear icon.
10. Leave the Clear Note empty and click Save.
11. Verify the success message and return to the Active Alarm table.
12. Close the Active Alarm window and return to Dashboard.
13. Open `System/Security/Access Log`.
14. Query from 15 seconds before Ack through 45 seconds after Clear.
15. Verify the Ack success description contains the remembered `(id,subid)`.
16. Verify the Clear success description contains the remembered `(id,subid)`.

## Expected Result

- The selected active alarm is acknowledged and cleared successfully.
- Access Log contains `[Alarm - acknowledge alarm] set success (acknowledge one alarm - (id,subid)=(<index_1>,<index_2>))`.
- Access Log contains `[Alarm - clear alarm] set success (clear one alarm - (id,subid)=(<index_1>,<index_2>))`.

## Automation Notes

- The case is skipped when Dashboard has no active alarm.
- Ack and Clear descriptions are searched only within the recorded operation-time interval.
- This case changes the first active alarm by acknowledging and clearing it.
- This case is marked `@pytest.mark.Unicase`.
