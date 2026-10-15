# EMS1-4029 / EMS1-6305 usrNodePermission

## Test flow

1. Create `usrNodePermitFunction` with ReadWrite / Global access restricted to the configured DUT, then log in with this test account.
2. Open System / System Properties / Alarm Notification. Set Warning Sound, Notify Critical Alarm, Notify Major Alarm, Notify Minor Alarm, and Notify Info Alarm to OFF. Click Save, acknowledge the response, and wait for the message dialog to close before testing permissions.
3. Check the five selected notification settings remain OFF.
4. Check node permissions across the existing Dashboard, Map, Alarm, Inventory, Performance, Maintenance, Provision, Script, and System pages.
5. For the Dashboard alarm popup and Alarm / Active and History tables, inspect only the first page. Do not traverse subsequent alarm pages. Preserve the existing device name/IP permission assertions and empty-table handling.

## Expected result

- Alarm notifications are OFF for the test account before permission checks start.
- First-page alarm rows satisfy the existing DUT/EMS visibility rules.
- Other page permission checks retain their existing behavior.

## Change note

- Added notification setup after test-account login and limited alarm data collection to page 1 to reduce runtime.
