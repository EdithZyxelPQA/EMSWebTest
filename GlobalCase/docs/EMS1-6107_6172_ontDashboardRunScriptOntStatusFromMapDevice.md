# EMS1-6107/6172 ontDashboardRunScriptOntStatusFromMapDevice

## Purpose

Verify ONT Dashboard Run Script and ONT status when the ONT Dashboard is opened from Map/Device/ONT Status.

## Test Data

Read the DUT and the configured ONTs from `environment_parameter.json`. The number of ONTs is controlled by `exe_ontCount`.

## Steps

1. Login to EMS Web and open `Map`.
2. Expand the navigation panel and select the configured device.
3. In the device `ONT Status` table, find each configured ONT by SN and open its ONT Dashboard.
4. Select and run the script matching the ONT type.
5. Verify the ONT title, SN, model, admin status, operation status, type, and updated description.
6. For XONT, also verify the command console content.

## Expected Result

Every configured ONT opens from Map/Device and passes the same Run Script and ONT status checks as EMS1-6077/6885.

## Automation Notes

This case is marked `@pytest.mark.Unicase` and reuses the EMS1-6077/6885 validation logic.
