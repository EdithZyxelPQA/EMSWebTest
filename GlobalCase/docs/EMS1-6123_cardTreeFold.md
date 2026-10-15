# EMS1-6123 cardTreeFold

## Purpose

Verify that all configured DUT cards are displayed when the device tree is expanded and hidden when it is folded.

## Test Data

Read from `environment_parameter.json`.

- EMS URL, username, and password
- DUT type, IP, device name, and Map node name
- DUT card slot IDs and card type names

## Preconditions

- The DUT exists and is online in the EMS Map.
- Card information in `environment_parameter.json` matches the cards installed in the DUT.
- OLT14xx devices are not supported by this case.

## Steps

1. If the DUT type contains `OLT14`, mark the case as skipped.
2. Login to EMS Web and open `Map`.
3. Click `navside_icon` and select the DUT.
4. Click the `+` icon beside the DUT.
5. Verify every valid configured card is visible and its text is `<slot ID> - <card type>`.
6. Click the `-` icon beside the DUT.
7. Verify every configured card is folded and no longer visible.

## Expected Result

- All configured cards appear after expanding the device node.
- All configured cards disappear after folding the device node.
- OLT14xx devices report SKIP instead of attempting the test.

## Automation Notes

- Card nodes are identified by the DUT `data-nodeid` plus each configured slot ID.
- Slot IDs `0` and `--` are ignored.
- This case is marked `@pytest.mark.Unicase`.
