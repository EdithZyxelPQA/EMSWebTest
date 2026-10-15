# EMS1-4361 Availability and Device Panel link

## Purpose

Verify that the equipment image displayed in Map/Device Status is identical to the image opened through the `Device panel` link, and verify that the dialog can be closed with its OK button.

## Test Steps

1. Login to EMS Web and open `Map`.
2. Select the DUT configured in `environment_parameter.json`.
3. Wait for the equipment image at the bottom of the device Status page (`#device_image img`).
4. Confirm that the image has a non-empty `data:image` source and save it in `report`.
5. Click the `Device panel` link.
6. Wait for `#device_panel_dialog_image img` and confirm that it has a non-empty `data:image` source.
7. Compare the complete image source with the Map Status equipment image; both must be identical.
8. Save the Device Panel image in `report`.
9. Find the enabled `.modal-xl .button` (prefer its text/value `OK`), click it, and wait until the Device Panel image is no longer visible.

## Expected Result

- Both equipment images load successfully.
- The Map Status and Device Panel images are identical.
- Clicking OK closes the Device Panel dialog completely.

## Automation Notes

- The case is marked `@pytest.mark.Unicase`.
- Individual checks use `with assume` so both image-loading and image-comparison results are reported.
- The case uses the common Map device-selection helper, including IP Filter and nested-submap expansion fallback.
