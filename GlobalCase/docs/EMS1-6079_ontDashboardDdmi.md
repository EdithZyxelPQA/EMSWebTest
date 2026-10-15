# EMS1-6079 ontDashboardDdmi

## Purpose

Verify that the DDMI charts on every configured in-service ONT Dashboard expose valid frontend data.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, and password
- DUT device name and Map node name
- `ONT.exe_ontCount`
- ONT1 through ONT`exe_ontCount`: SN, slot, port, and ONT ID

## Preconditions

- The DUT exists and is online in EMS.
- Every ONT selected by `exe_ontCount` is in service and appears in Dashboard/ONT Status.
- The ONT Dashboard DDMI section has loaded Chart.js data.

## Steps

1. Login to EMS Web.
2. Open `Dashboard`.
3. In `ONT Status`, click `InService`.
4. Open the device filter and select the configured DUT.
5. For each ONT from ONT1 through ONT`exe_ontCount`:
   1. Find the ONT row by serial number and double-click it.
   2. Switch to the newly opened ONT Dashboard window.
   3. Read every Chart.js dataset in the DDMI section.
   4. Verify each dataset contains between 1 and 96 points, including empty-value points.
   5. Allow positive, negative, zero, and empty values, but verify each dataset contains at least one numeric value.
   6. Close the ONT Dashboard and return to the main EMS window.

## Expected Result

- Every configured ONT can open its ONT Dashboard.
- The DDMI section contains Chart.js data.
- Every DDMI dataset contains between 1 and 96 points.
- DDMI values may be positive, negative, zero, or empty.
- Every DDMI dataset contains at least one numeric value.

## Automation Notes

- The Dashboard row-opening flow reuses the pattern from EMS1-6077/6885.
- Chart data is read directly from Chart.js, following the EMS1-7071 approach.
- This case is marked `@pytest.mark.Unicase`.
