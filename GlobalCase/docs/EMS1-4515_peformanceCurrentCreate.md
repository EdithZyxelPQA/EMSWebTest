# EMS1-4515 peformanceCurrentCreate

## Objective

Verify that EMS can create Performance/Current demand charts for the test device NXC interface, and that probe count and chart titles are correct. Chart series data is outside this Case's scope.

## Test Data

- EMS URL: from `environment_parameter.json`
- EMS account: from `environment_parameter.json`
- DUT: `ZYXEL_DUT.<cmdopt>`
- Card: `CARDINFO.NXC`
- Test port: `CARDINFO.NXC.port_id`

## Steps

1. Login EMS Web.
2. Go to `Performance/Current`.
3. If any chart is already open, click every chart `X` button to close all charts.
4. Click the `Create` icon.
5. Check `The currently available number of probes is : <number>` is greater than or equal to `100`.
6. Select `Performance Type = Interface(Accumulation)`.
7. In `Device List`, expand the test device.
8. Select the NXC card from `CARDINFO.NXC`.
9. Select the NXC test port from `CARDINFO.NXC.port_id`.
10. Click `Create`.
11. Return to `Performance/Current`.
12. Wait up to 30 seconds for a new chart to appear; chart data is not required.
13. Verify a new chart appears.
14. Verify chart title:
    `Interface(Accumulation) : <Node Name>(<Device IP>) - <Card Info Type>(<slot id>) - <port id>, Polling : 1 Minutes`
15. Click the `Create` icon again.
16. Check the available probe count is the previous value minus `1`.
17. Select `Performance Type = Interface(Rate)`.
18. Select the same test device, NXC card, and NXC test port.
19. Click `Create`.
20. Return to `Performance/Current`.
21. Wait up to 30 seconds for the second chart to appear; chart data is not required.
22. Verify a new chart appears.
23. Verify chart title:
    `Interface(Rate) : <Node Name>(<Device IP>) - <Card Info Type>(<slot id>) - <port id>, Polling : 1 Minutes`
24. Click every chart `X` button to close all charts.

## Expected Result

- Available probe count is at least `100` after existing charts are closed.
- Creating the first chart decreases available probe count by `1`.
- `Interface(Accumulation)` chart appears with the expected title; series data is not checked.
- `Interface(Rate)` chart appears with the expected title; series data is not checked.
- All charts are closed at the end of the test.
