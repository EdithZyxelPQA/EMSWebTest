# EMS1-6262 ontServiceSelectBySearch

## Purpose

Verify that EMS can create an ONT service by searching and selecting an unregistered ONT by Serial Number.

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

## Preconditions

- DUT can be reached by SSH.
- EMS Web can be reached by browser.
- The test ONT is physically discoverable by the DUT after remote interface deletion.
- Browser driver is available for the configured browser.
- Python dependencies in `requirements.txt` are installed.

## Automated Steps

1. Read `exe_provision_ont` from `environment_parameter.json`.
2. Read the selected ONT data from `ZYXEL_DUT.<node>.ONT.<exe_provision_ont>`:
   - `sn_16`
   - `pw`
   - `flag`
3. SSH to DUT `192.168.168.85`.
4. Because `flag` is `xont`, send:

   ```text
   no interface remote xont sn 5A5958458CACE176
   no interface remote xont registration-id D41AD1009ED8
   ```

5. If the DUT prompts for delete confirmation, send `y`.
6. Open EMS Web URL.
7. Log in to EMS.
8. Go to `Inventory / ONT`.
9. Filter by ONT Serial Number `5A5958458CACE176`.
10. Wait until exactly one ONT row is found and its `ONT ID` is `Unregistered`.
11. Go to `Provision / Service / ONT`.
12. Filter by ONT Serial Number `5A5958458CACE176`.
13. If an existing ONT service row is found, select and delete it.
14. Click `New Service`.
15. In `Create ONT Service`, click `Select ONT`.
16. In the Select ONT dialog, enable the SN filter, enter the SN, and click the normal `Search` button.
17. If SN search does not find the row, retry by 12-digit SN and then by DUT IP while still matching the target SN/password.
18. Select the row whose SN matches `5A5958458CACE176` or its 12-digit form and whose password matches `D41AD1009ED8`.
19. Click `OK`.
20. In `Create ONT Service`, open the `{}` editable service row.
21. In `Edit ONT Service`, enable `Active`.
22. In the `Description` field, enter `testSearchUnregistered`.
23. Click `OK`.
24. Back in `Create ONT Service`, click `Save`.
25. Confirm the EMS message dialog.
26. Return to `Provision / Service / ONT`.
27. Filter by ONT Serial Number `5A5958458CACE176`.
28. Wait until the service `Status` becomes `Success`.
29. Go to `Inventory / ONT`.
30. Filter by ONT Serial Number `5A5958458CACE176`.
31. Wait until exactly one ONT row is found and its `ONT ID` is not `Unregistered`.
32. Verify the ONT `description` field is `testSearchUnregistered`.

## Expected Result

- The ONT is first shown as `Unregistered` in `Inventory / ONT`.
- EMS creates a new ONT service by selecting the ONT through the Select ONT dialog.
- The ONT service status becomes `Success`.
- The ONT is later shown in `Inventory / ONT` with an `ONT ID` other than `Unregistered`.
- The ONT `description` field in `Inventory / ONT` is `testSearchUnregistered`.
- Test case result is PASS.

## Actual Run

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_ems1_6262_ont_service_select_by_search.py::TestEMS16262OntServiceSelectBySearch::test_EMS1_6262_ontServiceSelectBySearch -v -s --cmdopt=192.168.168.85
```

Result:

```text
1 passed in 288.50s (0:04:48)
```
