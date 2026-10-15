# EMS1-4903 powerSupplyDisplay

## Purpose

Verify that the Power Supply modules shown in the Map/Device equipment image match `hwinfo.power` in the device RESTful dev JSON.

## Supported devices

OLT14xx devices do not support RESTful device information. When the DUT type contains `OLT14`, this case reports SKIP immediately and does not execute SNMP operations, RESTful debug collection, or equipment-image comparison.

## RESTful Debug Collection

1. Read and preserve the current values of these four Net-SNMP MIB objects:
   - `emsUploadUuid_dev` (`...16.21.1`)
   - `emsUploadPath_dev` (`...16.21.2`)
   - `emsUploadUuid_perf` (`...16.21.5`)
   - `emsUploadPath_perf` (`...16.21.6`)
2. For NeoX devices use base OID `1.3.6.1.4.1.890.1.5.19.1.16.21`; other supported families use the existing EMS base OID `1.3.6.1.4.1.890.1.5.13.13.16.21`.
   The configured SNMP version is tried first. If SNMPv3 authentication times out, the case retries with the DUT's configured SNMPv2C get/set communities and then uses that same working protocol for backup, modification, and restoration.
3. Set the dev UUID to `<device ip>_dev` and its path to `https://<EMS IP>/RESTfulServer/Server/DevicePollerDebug/`.
4. Set the performance UUID to `<device ip>_perf` and its path to `https://<EMS IP>/RESTfulServer/Server/PerformanceDebug/`.
5. SSH to the EMS Server, enter `/opt/ELEMENTVIEW_MASTER/bin`, make both generated files readable, and download `<device ip>_dev` and `<device ip>_perf` into `report`.
6. Restore all four MIB values in `finally`, including when download, JSON parsing, Web navigation, or image validation fails.

## Test Steps

1. Parse the downloaded dev JSON and require a non-empty `hwinfo.power` list.
2. Login to EMS Web, open `Map`, and select the configured DUT.
   If the DUT is not found after expanding the visible submaps, enter its IP in the Map tree Filter and search again.
3. Read the equipment image at the bottom of the device Status page.
4. Select a relative-coordinate image profile by device type. Relative coordinates are based on the original image size and are unaffected by browser zoom or display scaling.
5. For every Power Supply entry, compare its RESTful `mode` with the profile and compare RESTful `status` with the corresponding image LED:
   - `up`: the LED region must contain the expected green pixels.
   - `down`: the LED region must not be green.
6. Click `Device panel`, wait for `#device_panel_dialog_image img`, and repeat the same mode/status/LED comparison against the Device Panel image.
7. Save both the Map Status equipment image and Device Panel image, plus both downloaded JSON files, in `report` as evidence.

## Supported Image Profiles

- `NeoX-06`: two DC Power Supply modules at the bottom of the equipment image.
- `NeoX-03`: two DC Power Supply modules at the bottom of its shorter equipment image, using a separate coordinate profile from NeoX-06. Its LED-on threshold is 40 green pixels so small green artwork fragments in an unlit module are not classified as an active PWR LED.
- `IES5206`: two DC Power Supply modules at the top of the equipment image.
- `IES4204`: two DC Power Supply modules at the upper-right of the equipment image; the profile samples the two small PWR LEDs rather than the large green terminal blocks.

An unknown device type is skipped with an explicit message instead of using an unsafe fixed coordinate from another model.

## Expected Result

- OLT14xx devices report SKIP because RESTful device information is unsupported.
- Both RESTful debug files are downloaded and contain valid JSON objects.
- `hwinfo.power` exists and contains the same number of entries as the device image profile.
- Every Power Supply mode and green/off LED state matches its RESTful entry.
- Both the Map Status image and the Device Panel image pass the same RESTful comparison.
- All four modified upload MIB values are restored to their recorded original values.

## Automation Notes

- The case is marked `@pytest.mark.Unicase`.
- The equipment drawing is a single base64 raster image, not separate PSU DOM elements; therefore Selenium selectors cannot directly read individual Power Supply states.
- LED classification uses green-channel dominance in a small area around each model-specific relative position.
- A model profile may override the default green-pixel threshold when its equipment artwork contains nearby green fragments.
- The base64 image sources are copied in one JavaScript operation so an EMS background refresh cannot leave Selenium with stale image elements.
- Assertions use `with assume` for individual Power Supply comparisons so all displayed modules are checked.
