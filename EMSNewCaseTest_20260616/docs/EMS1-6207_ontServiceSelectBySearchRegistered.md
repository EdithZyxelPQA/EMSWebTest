# EMS1-6207 ontServiceSelectBySearchRegistered

## Purpose

Verify that EMS can create an ONT service by searching and selecting an already registered ONT by Serial Number.

## Test Data

Data source: `EMSNewCaseTest_20260616/environment_parameter.json`

- EMS URL: `https://192.168.128.100:9116/netatlasems/index`
- EMS user: `admin`
- DUT: `192.168.168.85`
- DUT user: `admin`
- Test ONT: `8-16-1`
- ONT SN: `5A5958458CACE176`
- ONT password: `D41AD1009ED8`
- ONT flag: `xont`

## Automated Steps

1. Read `exe_provision_ont` from `environment_parameter.json`.
2. Read the selected ONT `sn_16`, `pw`, `flag`, `slot_id`, `port_id`, and `ont_id`.
3. Open EMS Web URL and log in.
4. Go to `Provision / Service / ONT`.
5. Filter by ONT Serial Number.
6. If an existing ONT service row is found, select and delete it.
7. SSH to the DUT.
8. Remove the ONT remote interface by SN and registration-id to force the ONT to become unregistered:

    ```text
    no interface remote xont sn 5A5958458CACE176
    no interface remote xont registration-id D41AD1009ED8
    ```

9. In EMS, go to `Inventory / ONT`.
10. Filter by the target slot and port, for example slot `8`, port `16`.
11. Read the existing ONT ID usage on that port.
12. Build the CLI registration candidate list from the configured ONT ID upward, excluding ONT IDs already occupied in EMS Inventory.
13. Enter `configure`.
14. Because `flag` is `xont`, register the ONT by CLI with the first unoccupied candidate AID:

    ```text
    interface remote xont 8-16-1
    sn 5A5958458CACE176
    registration-id D41AD1009ED8
    no inactive
    exit
    ```

15. If the selected candidate is unavailable, retry only with the next EMS-unoccupied candidate; do not enter or modify an ONT ID already occupied in EMS Inventory.
16. Go to `Inventory / ONT`.
17. Filter by ONT Serial Number.
18. Wait until exactly one ONT row is found and its `ONT ID` matches the ONT ID registered by CLI.
19. Go to `Provision / Service / ONT`.
20. Click `New Service`.
21. In `Create ONT Service`, click `Select ONT`.
22. In the Select ONT dialog, enable the SN filter, enter the SN, and click the normal `Search` button.
23. Select the row whose SN/password matches the test ONT, then click `OK`.
24. In `Create ONT Service`, open the `{}` editable service row.
25. In `Edit ONT Service`, enable `Active`.
26. In the `Description` field, enter `testSearchRegistered`.
27. Click `OK`.
28. Back in `Create ONT Service`, click `Save`.
29. Confirm the EMS message dialog.
30. Return to `Provision / Service / ONT`.
31. Filter by ONT Serial Number.
32. Wait until the service `Status` becomes `Success`.
33. Go to `Inventory / ONT`.
34. Filter by ONT Serial Number.
35. Wait until exactly one ONT row is found, its `ONT ID` is not `Unregistered`, and its `description` is `testSearchRegistered`.

## Expected Result

- Any existing ONT service for the target SN is removed before the test.
- The target ONT is removed by both SN and registration-id/password before registration.
- The CLI registration AID is chosen from EMS Inventory/ONT slot/port data and does not modify occupied ONT IDs.
- The ONT is registered on the DUT by CLI.
- EMS Inventory shows the ONT ID registered by CLI.
- EMS creates a new ONT service by selecting the registered ONT through the Select ONT dialog.
- The ONT service status becomes `Success`.
- EMS Inventory shows the ONT with an `ONT ID` other than `Unregistered`.
- EMS Inventory shows the ONT `description` as `testSearchRegistered`.
- Test case result is PASS.
