# EMS1-6108/6171 ontDashboardRebootAlarmFromMapDevice

## Purpose

Verify ONT Dashboard reboot and alarm behavior when the ONT Dashboard is opened from Map/Device/ONT Status.

## Test Data

Read the DUT and the configured ONTs from `environment_parameter.json`. The number of ONTs is controlled by `exe_ontCount`.

## Steps

1. Login to EMS Web and prepare Alarm Severity and Pairwise Correlation settings.
2. Open `Map`, expand the navigation panel, and select the configured device.
3. In the device `ONT Status` table, find each configured ONT by SN and open its ONT Dashboard.
4. Reboot the ONT and verify its alarm status.
5. Open Active Alarm, verify its export, and execute the supported alarm operations.
6. Restore the alarm settings after validation.

## Expected Result

Every configured ONT opens from Map/Device and passes the same reboot and alarm checks as EMS1-6078/6884.

## Automation Notes

This case is marked `@pytest.mark.Unicase` and reuses the EMS1-6078/6884 validation logic.
