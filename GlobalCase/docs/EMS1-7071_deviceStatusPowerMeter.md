# EMS1-7071 deviceStatusPowerMeter

## Scope

- Supported device type: NeoX only.
- EMS: use `environment_parameter.json`.
- DUT: use `--cmdopt` node from `environment_parameter.json`.

## Test Flow

1. Login EMS Web.
2. Enter `Map`.
3. Click `navside_icon` to expand the left tree.
4. Expand the tree by clicking `>` icons until the DUT is visible.
5. Select the DUT node.
6. Confirm the device detail page opens on the `Status` tab.
7. Read the `Power Meter` chart from frontend Chart.js data on canvas `map_char_powermeter`.
8. Confirm the chart exposes numeric data.
9. Confirm the time range from the first data point to the latest data point is within `25` hours.
10. Confirm the latest data value is greater than `0`.
11. Print the latest Power Meter data.

## Expected Result

`[EMS1-7071][deviceStatusPowerMeter] Result passed`
