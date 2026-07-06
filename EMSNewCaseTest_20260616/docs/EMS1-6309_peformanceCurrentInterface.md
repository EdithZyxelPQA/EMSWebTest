# EMS1-6309 peformanceCurrentInterface

## Objective

Verify that EMS can create Performance/Current charts for every interface port on each card of the test device, using `Interface(Accumulation)` and `Interface(Rate)` one card at a time.

## Test Data

- EMS URL/account: from `environment_parameter.json`
- DUT: `ZYXEL_DUT.<cmdopt>`
- Device name: `name_display`
- Cards/ports: discovered from `Performance/Current` Create dialog by expanding the DUT card list and reading each card's available port options

## Steps

1. Login EMS Web.
2. Go to `Performance/Current`.
3. Close every existing Performance chart.
4. For the first interface card on the DUT, discover all available ports in the Create dialog.
5. Create `Interface(Accumulation)` Performance/Current charts for every discovered port on that card.
6. Wait about 2 minutes and refresh the page.
7. Verify the expected chart title for every created chart:
   `Interface(Accumulation) : <Node Name>(<Device IP>) - <Card Info Type>(<slot id>) - <port id>, Polling : 1 Minutes`
8. Verify every chart exposes numeric values from the chart canvas hover tooltip.
9. Close every Performance chart.
10. For the same card, discover all available ports again.
11. Create `Interface(Rate)` Performance/Current charts for every discovered port on that card.
12. Wait about 2 minutes and refresh the page.
13. Verify the expected chart title for every created chart:
   `Interface(Rate) : <Node Name>(<Device IP>) - <Card Info Type>(<slot id>) - <port id>, Polling : 1 Minutes`
14. Verify every chart exposes numeric values from the chart canvas hover tooltip.
15. Close every Performance chart.
16. Repeat steps 4 to 15 for the next card until every supported interface card has been tested.

## Expected Result

- All existing Performance/Current charts are closed before testing.
- For each card, all ports exposed by the Create dialog can create `Interface(Accumulation)` charts.
- For each card, every `Interface(Accumulation)` chart has the expected title and numeric canvas values.
- All `Interface(Accumulation)` charts are closed before testing `Interface(Rate)` on the same card.
- For each card, all ports exposed by the Create dialog can create `Interface(Rate)` charts.
- For each card, every `Interface(Rate)` chart has the expected title and numeric canvas values.
- All charts are closed before moving to the next card and at the end of the test.
