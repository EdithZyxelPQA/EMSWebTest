# EMS1-7226 reprovisionInDeletedDevice

## Purpose

Verify an ONT service can return to `Wait` after its device is deleted from Map Management, can be edited while the device is deleted, and can reprovision to `Success` after the same device is added back.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, password
- DUT IP, DUT login username, DUT login password
- Provision ONT SN, password/registration ID, slot, port, ONT ID, ONT flag
- DUT Map Management fields such as device name, description, SNMP community, SSH port, and geo position

## Preconditions

- The test ONT exists physically and can become `Unregistered` in Inventory/ONT after CLI unregistration.
- The test device exists in `System/Security/Map Management` before the delete step.
- This case deletes and re-adds the DUT in EMS Map Management. If the test aborts after deletion, the automation attempts to add the device back with the remembered settings.

## Steps

1. SSH to the DUT and unregister the test ONT.
   - `xont`: `no interface remote xont sn <sn>` and `no interface remote xont registration-id <pw>`
   - `ont`: `no interface remote ont sn <sn>` and `no interface remote ont password <pw>`
   - `ont-14`: `configure`, `no interface remote ont sn <sn>`, and `no interface remote ont password <pw>`
   - If the device asks for delete confirmation, answer `y`.
2. Login to EMS Web.
3. Open `System/Security/Map Management` and ensure the DUT exists. If a previous interrupted run left the DUT deleted, add it back using `environment_parameter.json` before continuing.
4. Open `Inventory/ONT`, filter `Serial Number` by the test SN, and wait for exactly one row whose `ONT ID` is `Unregistered`.
5. Open `Provision/Service/ONT`, filter by the test SN, and delete the existing service if it exists.
6. Click `New Service`.
7. Enter the test ONT SN in `Serial Number`.
8. Enter the test ONT password in `Password/Registration ID`.
9. Double-click the `{}` cell to open `Edit ONT Service`.
10. Enable `Active`.
11. Enter `beforeDeleteDevice` in `Description`.
12. Click `OK`, then click `Save`. Capture the resulting EMS message before closing it and stop immediately with the actual message text unless it contains `success`.
13. After EMS reports success, filter the Service table by the test SN and require the new row to appear within 30 seconds. Then wait for the ONT service status to become `Success`.
14. Open `Inventory/ONT`, filter by the test SN once, then use `Refresh` to wait for exactly one row whose `ONT ID` is not `Unregistered` and whose `description` is `beforeDeleteDevice`.
15. Remember the ONT AID from `Slot`, `Port`, and `ONT`.
16. Open `System/Security/Map Management`.
17. Select the DUT in the device list, click `Edit`, and remember the DUT settings shown in the edit form.
18. Select the DUT again, click `Delete`, and confirm.
19. Open `Provision/Service/ONT` and wait for the test SN service status to become `Wait`.
20. Click the service `Modify/Edit` link, change only the `Description` field to `afterDeleteDevice`, and click `OK`. Close `#modal_service_profile_info` and wait until both the dialog and its modal backdrop have completely disappeared.
21. Open `System/Security/Map Management`.
22. Select `EMS`, click `Add`, enter the remembered DUT settings, save, and confirm.
23. Open `Provision/Service/ONT` and wait for the test SN service status to become `Success`.
24. Only after the ONT service status is `Success`, open `Inventory/ONT`, filter by the test SN once, then use `Refresh` to wait for exactly one row whose `ONT ID` is not `Unregistered`.
25. Verify the `description` column in `Inventory/ONT` is `afterDeleteDevice`.

## Expected Result

- The ONT service reaches `Success` before the device is deleted.
- Before deleting the DUT, `Inventory/ONT` shows the ONT ID is not `Unregistered` and description is `beforeDeleteDevice`.
- After deleting the DUT from Map Management, the same ONT service returns to `Wait`.
- The ONT service can be edited while the DUT is deleted.
- After adding the DUT back with the remembered settings, the same ONT service returns to `Success`.
- In `Inventory/ONT`, the ONT ID is not `Unregistered`.
- In `Inventory/ONT`, the description is `afterDeleteDevice`.

## Automation Notes

- All EMS operations are performed through the web UI by Selenium.
- DUT ONT unregistration is performed by SSH because this is part of the setup condition.
- Manual ONT Service creation validates the EMS response text before closing the dialog. An EMS error is reported immediately instead of being hidden and followed by a 600-second empty-table wait.
- Even after an EMS success response, the newly created service row must become visible within 30 seconds before the longer provisioning-status wait begins.
- After editing the Wait service description, the automation explicitly closes the ONT Service Profile dialog and waits for its backdrop to disappear before navigating to Map Management. This prevents the dialog from intercepting the `System` menu click.
- At startup, the automation repairs the precondition by adding the DUT back if a previous interrupted run left it deleted from Map Management. The fallback add operation uses the DUT's configured SNMP version, Get/Set communities, SNMPv3 fields, and geo position from `environment_parameter.json`.
- The automation uses the values in `environment_parameter.json` as fallback Map Management settings, then overwrites them with values read from the DUT edit form when available.
