# EMS1-4362_4398 deviceHwMonitor

## Purpose

Verify the Map/Device CPU, Memory, Fan, Temperature, and Voltage hardware-monitor status, including low/high threshold alarms and restoration.

## Test Data

Read the EMS URL, DUT credentials, device type, Map node, device IP, and configured card slot IDs from `environment_parameter.json`.

## Steps

1. SSH to the configured DUT and reset hardware-alarm thresholds to their defaults. OLT14 uses `no hw-monitor fan-speed-threshold all`, `no hw-monitor temperature-threshold all`, and `no hw-monitor voltage-threshold all` under configuration mode. Other supported devices retain the existing `no hw-monitor` reset command. Stop the case if the CLI reports Invalid, Error, or Out of Range.
2. Login to EMS Web, open `Map`, and select the configured DUT.
3. Verify CPU, Memory, and Fan icons render and expose non-empty status text.
4. For every configured card slot except `0` and `--`, run `show hw-monitor <slot>` and `show hw-monitor statistics <slot>` over SSH. For an OLT14 device, run `show hardware-monitor C` once because the fixed chassis has no selectable card slot and the same output contains Current and threshold values.
5. Parse every Temperature and Voltage monitor's Name, Index, default High/Low thresholds, Current value, and unit after the reset. For OLT14, also parse every Fan's Name, inferred Index, Current RPM, and default minimum RPM Threshold. OLT14 Voltage values and thresholds use decimal V values in the show output; other supported devices keep their existing CLI units.
6. On OLT14, test every Fan index first. Set its minimum RPM threshold above Current within `0..15000`, click EMS Refresh while polling, and verify the Fan icon changes and the accumulated warning contains Name, `too low`, Current RPM, and configured Threshold RPM.
7. Restore every changed OLT14 Fan threshold to its initially captured default value and wait for the Fan icon/status to return to Normal.
8. For every Temperature index, raise Low above Current while keeping High greater than Low. Keep the value within the device's original legal range; if no legal threshold exists between Current and default High, skip only that monitor/direction and continue.
9. Click the EMS Refresh icon while polling. Wait for the Temperature warning and verify its Slot when supplied by EMS, sensor Name, `too low`, Current value and unit, and configured Low threshold and unit. Verify warnings accumulate as each index is changed, and independently verify the icon appearance differs from its Normal baseline.
10. Restore all default Temperature thresholds and wait for the icon/status to return to Normal.
11. Lower High below Current while keeping High greater than Low. Keep the value within the device's original legal range; if no legal threshold exists between default Low and Current, skip only that monitor/direction. Verify the accumulated `too high` warnings and configured High thresholds.
12. Restore the default Temperature thresholds again and wait for Normal.
13. Repeat the low/high tests and restoration for every Voltage index.

For OLT14, configure and restore each monitor with `hw-monitor fan-speed-threshold <index> <threshold>`, `hw-monitor temperature-threshold <index> <high> <low>`, or `hw-monitor voltage-threshold <index> <high> <low>`. These commands intentionally omit `cardtype` and `slot`. Temperature values are sent directly in degrees Celsius and must remain within `-50..106`. OLT14 `show hardware-monitor C` displays Voltage in V, while both the threshold CLI and EMS warning text use integer mV within `0..25000`; the case therefore converts the parsed V values to mV for both command construction and warning comparison. A 1 mV threshold display difference is accepted. Fan threshold input and EMS comparison use RPM within `0..15000`.

## Expected Result

- CPU, Memory, and Fan status render correctly.
- Every configured Temperature and Voltage index produces the correct low and high warning information. Every OLT14 Fan index produces the correct low-speed warning information.
- Warning information accumulates for all changed indexes.
- Each warning is parsed and compared as one complete row, so a Threshold from a different sensor cannot be paired with the current expected sensor.
- Fan, Temperature, and Voltage return to Normal after their original thresholds are restored.

## Safety and Automation Notes

- The case is marked `@pytest.mark.Unicase` and is enabled for execution.
- OLT14 resets only the three threshold groups with their `no hw-monitor <kind>-threshold all` commands. A standalone `no hw-monitor` is an incomplete OLT14 command and is not sent. Other supported devices retain their existing reset command.
- Default threshold values are captured after the reset and before any test-specific change.
- For OLT14, `genni`, and `nni`, the command is `hw-monitor <kind>-threshold <index> <high> <low>`. Other card types use `hw-monitor <kind>-threshold cardtype <cardtype> slot <slot> <index> <high> <low>`.
- The `too low` phase restores every attempted monitor to the default High/Low values captured after `no hw-monitor` in `finally`, including when the CLI check or UI verification fails. The `too high` phase has a separate `finally` restoration with the same guarantee.
- Warning content and abnormal-icon mismatches are recorded with `with assume`, so one monitor or the `too low` direction failing does not prevent remaining monitors or the `too high` direction from running.
- Temperature warnings compare Slot when present, sensor Name, direction, Current, Threshold, and unit. Voltage names reported by EMS can differ from the CLI monitor names, so Voltage warnings are paired by Slot when present, direction, configured Threshold, Current tolerance, and unit; each displayed warning row can be used only once. OLT14 voltage expectations are normalized from V to the EMS warning's mV before comparison.
- CLI configuration/restoration failures and failure to return to Normal remain hard failures; the case does not continue changing thresholds while the device may be in an unsafe or unknown state.
- After each restoration, the case clicks Refresh while polling until the corresponding icon/status returns to Normal.
- The case may take several minutes because EMS hardware-monitor status is polled after each CLI change.
