# EMS1-6090 ontStatusSort

## Scope

- EMS: use `environment_parameter.json`.
- Page: `Dashboard`.
- Dashboard block: `ONT Status`.
- Table: `All_ontStatusTable`.

## Test Flow

1. Login EMS Web.
2. Enter `Dashboard`.
3. Read the clickable status entries shown in the `ONT Status` block from the current EMS UI.
   - Status names are not hard-coded because ONT Status and Ethernet Access Port Status may have different status sets.
4. For each clickable ONT Status entry:
   - Click the status number/name from the Dashboard UI.
   - Print the Dashboard status number and the opened table `Total data`.
   - Do not assert these two numbers are equal in this sort case because the Dashboard summary and opened table may use different aggregation scopes on some EMS servers.
   - If `Total data` is `0`, skip sort verification for this status because there are no rows to sort.
   - Detect every visible sortable column in `All_ontStatusTable`.
   - Scroll each visible column title into view with Selenium `location_once_scrolled_into_view`.
   - Click the visible column title until the sort icon becomes `date-type="extend"`, then verify each current table page is sorted ascending.
   - Click the same visible column title until the sort icon becomes `date-type="hide"`, then verify each current table page is sorted descending.
   - When moving to the next page, do not click the column title again and do not re-check direction. Only validate the table data displayed on that page.
   - Each page is validated independently with the data displayed at that moment.
   - If the table becomes empty after sorting or paging while `Total data` is not `0`, judge the case as failed. This indicates the EMS Dashboard table did not keep valid visible data during the user paging flow.

## Sort Rules

- `IP Address` is checked by IP address order.
- `Device Type` is checked by EMS device type order.
- `Alarm Status` is checked by EMS alarm severity order.
- Other text column values are checked by the EMS table's displayed ordering behavior: comparison is case-insensitive, and `_` is ordered after letters, digits, and `.`.

## Expected Result

`[EMS1-6090][ontStatusSort] Result passed`
