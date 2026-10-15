# EMS1-6156/6144/6145 deviceDashboardAlarmAckClear

## Purpose

Verify the alarm status, acknowledge, and clear operations from the selected device dashboard on Map.

## Test Data

Read the EMS URL, credentials, DUT Map node name, device name, and device IP from `environment_parameter.json`.

## Preconditions

- The configured DUT exists in EMS Map.
- The DUT has at least one active alarm. If it has no active alarm, the case is skipped.

## Steps

1. Login to EMS Web and open `Map`.
2. Select the configured device.
3. Confirm that device Alarm Status contains at least one active alarm.
4. Click the Alarm Status total and then `more...` to open today's device Active Alarm window.
5. Verify that every `Device IP` value in the complete Active Alarm table equals the configured DUT IP.
6. Select the first row and record its `index_1` and `index_2`.
7. Click Ack and accept the success message.
8. Find the same row by `index_1` and `index_2`, then select it and click Clear.
9. Enter `$py_clearTime: <current time>` using `%Y-%m-%d_%H:%M:%S` format and save the clear note.
10. Accept the success message and confirm that the cleared row no longer exists in the Active Alarm table.
11. Close the Active Alarm window and return to Map/Device.

## Expected Result

- The first active alarm can be acknowledged successfully.
- Every Active Alarm row belongs to the configured DUT IP.
- The same alarm can be cleared with the required clear note.
- The cleared alarm disappears from the device Active Alarm table.
- The browser returns to the original Map/Device window.

## Automation Notes

This case is marked `@pytest.mark.Unicase`.
