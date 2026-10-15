# EMS1-7099 statusOntTest

## Objective

Verify that Inventory/ONT Information displays the expected DUT CLI commands for every configured test ONT.

## Test Data

- EMS URL and account: `environment_parameter.json`
- DUT and ONTs: `ZYXEL_DUT.<cmdopt>`
- Expected command format: selected by each ONT `flag` (`xont`, `ont`, or `ont-14`)

## Steps

1. Open `Inventory / ONT`.
2. For every configured test ONT, filter by DUT IP, Slot, Port, and ONT ID.
3. Open the row's `Information` dialog.
4. Wait for the status output and verify all commands expected for that ONT flag.
5. Locate the dialog from `id="inventory_status_message"`. Support jQuery UI (`.ui-dialog`), `role="dialog"`, and Bootstrap modal containers; if none exists, use the nearest ancestor containing a visible Close control. Click Close and wait until the status message is no longer visible.
6. Continue with the next configured ONT.

## Expected Result

- Every required status command is present in the Information output.
- The Information dialog closes completely after each ONT check.
- Closing does not depend on a Bootstrap `.modal` class or the dialog's absolute position under the HTML body.
