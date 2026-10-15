# EMS1-4907 Login Success Alarm

## Purpose

Verify that opening a DUT Remote Control session produces a `Login Success` Active Alarm for the DUT.

## Marker

`@pytest.mark.Unicase`

## Supported devices

OLT14xx devices do not generate a `Login Success` alarm. When the DUT type contains `OLT14`, this case reports SKIP immediately and does not execute the device-time, SNMP, Remote Control, or Alarm query steps.

## Preconditions and CLI checks

1. SSH to the DUT and execute `show time`.
   The parser supports the existing single-line date/time formats.
2. Verify that the DUT time is within 120 seconds of the test host and the timezone is `+0800`.
3. If the time is incorrect, execute:
   - `configure`
   - `time server`
   - `time server address 216.239.35.4`
   - `time server type ntp`
   - `time timezone 0800`
   - `time server sync`
4. `Error: the ntp server existed` is accepted; other CLI errors are reported.
5. Read `show running-config` and locate the active `snmp-server version`.
6. Verify that at least one `snmp-server trap-destination` index points to the EMS server with the same SNMP version.
7. If no matching destination exists, configure an unused destination index for the EMS server and active SNMP version.

## EMS Web steps

1. Open **Map**, select the DUT, and record the time immediately before clicking **Remote Control**.
2. Wait until the `#` prompt appears inside `id="console"`, confirming that device login is complete.
3. Open **Alarm / Active** and click **Filter**.
4. Select the DUT in **Target**.
5. Set From Time to one minute before the Remote Control click and To Time to one minute after the filter is opened.
6. Click **Query**.
7. Refresh and retry for up to 120 seconds while waiting for the trap.

## Expected result

- OLT14xx devices report SKIP because this alarm is unsupported.
- A `Login Success` alarm is present for the DUT IP.
- Its Log Time is inside the recorded Remote Control time range.
