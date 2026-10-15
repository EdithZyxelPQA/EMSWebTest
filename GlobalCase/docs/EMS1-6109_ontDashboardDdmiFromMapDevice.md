# EMS1-6109 ontDashboardDdmiFromMapDevice

## Purpose

Verify ONT Dashboard DDMI chart data when the ONT Dashboard is opened from Map/Device/ONT Status.

## Test Data

Read the DUT and the configured ONTs from `environment_parameter.json`. The number of ONTs is controlled by `exe_ontCount`.

## Steps

1. Login to EMS Web and open `Map`.
2. Expand the navigation panel and select the configured device.
3. In the device `ONT Status` table, find each configured ONT by SN and open its ONT Dashboard.
4. Read every DDMI Chart.js dataset.
5. Verify each dataset has 1 to 96 points and contains at least one numeric value; negative, zero, and empty values are allowed.

## Expected Result

Every configured ONT opens from Map/Device and its DDMI data passes the same validation as EMS1-6079.

## Automation Notes

This case is marked `@pytest.mark.Unicase` and reuses the EMS1-6079 validation logic.
