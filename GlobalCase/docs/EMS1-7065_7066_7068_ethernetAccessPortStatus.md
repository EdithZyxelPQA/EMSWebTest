# EMS1-7065 / EMS1-7066 / EMS1-7068 ethernetAccessPortStatus

## Purpose

Verify Dashboard / Ethernet Access Port Status for `Up`, `Down`, and `Device Not Responding`.

## Preconditions

- EMS Web is reachable.
- The test account can log in to EMS.
- Dashboard contains the Ethernet Access Port Status widget.

## Test Steps

1. Log in to EMS Web.
2. Enter `Dashboard`.
3. Verify the `Ethernet Access Port Status` widget contains these statuses:
   - `Up`
   - `Down`
   - `Device Not Responding`
4. Click `Up`.
5. Record the number shown in the `Up` status block.
6. Verify the opened table `Total data` equals the `Up` status number.
7. Verify every row on the current table page has `Operation Status` equal to `Up`.
8. If the table has multiple pages, click the next page button and verify every page.
9. Repeat steps 4 to 8 for `Down`.
10. Repeat steps 4 to 8 for `Device Not Responding`.

## Expected Result

`[EMS1-7065/7066/7068][ethernetAccessPortStatus] Result passed`

- The three status blocks exist.
- Each status number equals the table `Total data`.
- Every row on every page has the selected `Operation Status`.
