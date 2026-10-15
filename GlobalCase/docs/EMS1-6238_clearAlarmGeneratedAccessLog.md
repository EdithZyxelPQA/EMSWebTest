# EMS1-6238 Clear alarm generated Access Log

## Purpose

Verify that clearing a device alarm from Map creates the corresponding System Access Log.

## Marker

`@pytest.mark.Unicase`

## Steps

1. Open **Map** and select the DUT from `environment_parameter.json`.
2. Record the current time and click the right-side **Clear Alarm** icon.
3. Confirm the message dialog.
4. Open **System / Security / Access Log**.
5. Click the right-side **Filter** icon.
6. Set Date From to one minute before the Clear Alarm click.
7. Set Date To to one minute after opening Access Log.
8. Click **Query** and wait up to 60 seconds for the Access Log.

## Expected result

The filtered Access Log contains this exact Description, using the DUT name and IP from the environment file:

```text
[Topology - clear device alarm] set success (device name=<device name>, IP address=<device IP>)
```

Example:

```text
[Topology - clear device alarm] set success (device name=NeoX_168.85, IP address=192.168.168.85)
```
