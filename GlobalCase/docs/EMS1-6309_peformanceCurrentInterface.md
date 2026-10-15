# EMS1-6309 peformanceCurrentInterface

## Objective

Verify that EMS can create valid Performance/Current charts for every port on every non-zero card slot, first with `Interface(Accumulation)` and then with `Interface(Rate)`.

## Test Data

- EMS URL/account: from `environment_parameter.json`
- DUT: `ZYXEL_DUT.<cmdopt>`
- Device name: `name_display`
- Cards/ports: discovered from `Performance/Current` Create dialog

## Steps

1. Go to `Performance/Current`.
2. If charts exist, quickly close all of them by clicking every `X` (`class="icon exitBlock"`).
3. Click the Create icon.
4. Wait 2 seconds and verify `The currently available number of probes is : N`. `N` must be greater than 0 before Create and must decrease by exactly 1 after every Create.
5. Select Performance Type `Interface(Accumulation)`. Do not select it again when it is already selected.
6. For chassis devices, under Device Type select the first card and its Port; every card whose Slot ID is not 0 must be tested. For an OLT140X-series device, do not select a Slot; select the device directly and test every available Port.
7. Click Create.
8. After returning to Current, immediately click Create again.
9. Repeat steps 4 to 8 until every Port on the current Slot has been created.
10. Wait 10 seconds, click Refresh, and verify that charts for every Port appear and all chart values are valid.
11. Quickly close all charts.
12. Repeat steps 3 to 11 until every non-zero Slot has been tested.
13. Repeat steps 3 to 12 using `Interface(Rate)`.

## Expected Result

- Existing charts are closed before creation starts.
- Every Create dialog is given exactly 2 seconds before its probe count is checked.
- Probe count is greater than 0 before Create and decreases by exactly 1 after every Create, including the final Port.
- After the fixed 2-second wait, if EMS still displays the previous probe count, the test polls the same Create dialog for up to 10 seconds for the expected decremented value instead of failing immediately.
- Performance Type is changed only when the requested type is not already selected.
- Every Port on every non-zero Slot is tested.
- For OLT140X-series devices, Slot selection is skipped and every Port exposed directly under the device is tested.
- No chart-presence check is performed between individual Create operations.
- After Create, the test waits for the Create modal to disappear, waits a fixed 1 second, and then clicks Create again. Alert/OK/error scanning runs only when the modal remains visible for more than 1 second.
- After all Ports on one Slot are created, the test waits 10 seconds, clicks Refresh, and verifies all charts and values together.
- All charts are quickly closed before moving to the next Slot.
- While closing charts, if an `X` is temporarily unavailable or a click does not remove the chart, wait 0.5 second, locate the currently visible `X` again, and retry up to three times before reporting an error.
- All Slots are tested with `Interface(Accumulation)` first and then with `Interface(Rate)`.
