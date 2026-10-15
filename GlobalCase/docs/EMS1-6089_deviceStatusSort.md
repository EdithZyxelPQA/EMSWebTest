# EMS1-6089 deviceStatusSort

## Scope

- EMS: use `environment_parameter.json`.
- DUT: use `--cmdopt` node from `environment_parameter.json`.
- Page: `Dashboard`.
- Dashboard block: `Device Status`.

## Test Flow

1. Login EMS Web.
2. Enter `Dashboard`.
3. Confirm the `Device Status` block includes these statuses:
   - `In Service`
   - `Linked`
   - `Disconnected`
4. Click the `In Service` count.
5. For each sortable table column:
   - Test every visible column that a user can operate, including columns to the right of `Contact` that require horizontal scrolling. Hidden DOM columns such as `DevID` are skipped.
   - Scroll the visible column title into view with Selenium `location_once_scrolled_into_view`.
   - Click the visible column title, such as `//*[@id="All_devStatusTable_head"]/thead/tr/th[1]` for `Submap Name`, at least once and repeat until the column icon becomes `date-type="extend"`.
   - Read the column values page by page.
   - Confirm each page is sorted in ascending order.
   - When moving to the next page, do not click the column title again and do not re-check the icon direction. Only validate that the current page data follows the selected sort direction.
   - Each page is validated independently with the table data displayed at that moment. The automation does not compare data between pages and does not keep old page values for later validation.
   - Return to the first page by clicking previous page until page 1, so the current sort state is preserved.
   - Scroll the same visible column title into view with Selenium `location_once_scrolled_into_view`.
   - Click the same visible column title at least once and repeat until the column icon becomes `date-type="hide"`.
   - Read the column values page by page.
   - Confirm each page is sorted in descending order.
   - When moving to the next page, do not click the column title again and do not re-check the icon direction. Only validate that the current page data follows the selected sort direction.
   - Each page is validated independently with the table data displayed at that moment. The automation does not compare data between pages and does not keep old page values for later validation.
   - Return to the first page by clicking previous page until page 1, so the current sort state is preserved.
   - `IP Address` is checked by IP address order.
   - `Device Type` is checked by EMS device type order.
   - `Alarm Status` is checked by EMS alarm severity order.
   - Other text column values are checked by the EMS table's displayed ordering behavior: comparison is case-insensitive, and `_` is ordered after letters, digits, and `.`.
   - Because Dashboard data can change during the test, each page is checked only against the data currently displayed after the user action. The test does not compare two reads of the same page and does not compare the descending data set with the ascending data set.
6. Repeat steps 4-5 for `Linked`.
7. Repeat steps 4-5 for `Disconnected`.

## Column Names

The automation uses the visible column title from `All_devStatusTable_head` in logs and reports. Sort direction is reported separately and must not be appended as part of the column name.

Example report wording:

- Column: `IP Address`; Direction: `ascending`
- Column: `Device Type`; Direction: `descending`

Internally, the EMS table also has DOM `name` attributes, for example:

- `Device Name`: `DevName`
- `IP Address`: `IPAddress`
- `Device Type`: `DevType`
- `Operational Status`: `DevStatus`
- `Alarm Status`: `DevAlarmStatus`

## Device Type Order

`Device Type` sorting uses this EMS order:

- `unknown`: 0
- `IES6000`: 8
- `IES5206`: 12
- `IES4204`: 19
- `IES5212`: 22
- `IES6217`: 23
- `OLT1404`: 25
- `OLT1408A-C`: 28
- `OLT1404B-IA`: 31
- `OLT1408B-IA`: 32
- `NeoX-06`: 33
- `NeoX-03`: 34

## Alarm Status Order

`Alarm Status` sorting uses this EMS order:

- `None`: 0
- `Critical`: 1
- `Major`: 2
- `Minor`: 3
- `Info`: 4

## Expected Result

`[EMS1-6089][deviceStatusSort] Result passed`
