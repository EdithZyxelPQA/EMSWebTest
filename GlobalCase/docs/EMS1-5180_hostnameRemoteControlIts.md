# EMS1-5180 hostnameRemoteControlIts

## Purpose

Verify that EMS Remote Control displays a hostname changed directly on the DUT and can restore the hostname through the Remote Control command field.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, and password
- DUT IP, SSH username, and SSH password
- DUT device name and Map node name

## Preconditions

- The DUT is reachable by SSH.
- The DUT exists and is online in the EMS Map.
- EMS Remote Control can establish a session with the DUT.

## Steps

1. SSH to the DUT.
2. Execute `configure`.
3. Execute `hostname SNET-RCPD-OLT`.
4. Login to EMS Web and open `Map`.
5. Select the DUT and open the `Remote Control` tab.
6. Wait until the console displays `SNET-RCPD-OLT`.
7. Enter `configure` in the Remote Control command field.
8. Enter `hostname <DUT name>` to restore the configured device name.
9. Wait until the console displays the restored DUT name.

## Expected Result

- Remote Control displays `SNET-RCPD-OLT` after the SSH hostname change.
- The DUT hostname is restored to the device name from `environment_parameter.json`.

## Automation Notes

- If the web restoration step fails, the automation attempts to restore the original hostname through SSH.
- This case is marked `@pytest.mark.Unicase`.
