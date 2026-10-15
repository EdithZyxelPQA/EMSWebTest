# EMS1-4363 ontStatusSort

## Purpose

Verify every sortable column of the Map/Device ONT Status table in descending and ascending order for every ONT status category.

## Test Data

Read the EMS URL and the DUT Map node from `environment_parameter.json`.

## Steps

1. Login to EMS Web, open `Map`, and select the configured DUT.
2. Confirm the ONT Status area contains `In Service`, `OOS-LO`, `OOS-NR`, `OOS-CD`, `OOS-NP`, `OOS-LS`, and `OOS-DG` in that order.
3. Click the number of `In Service` and verify its dashboard count matches the ONT Status table total.
4. For every visible sortable column, select descending order and verify the column values are descending on every page. Return to page 1 after checking all pages.
5. Select ascending order for the same column and verify the column values are ascending on every page. Return to page 1 after checking all pages.
6. Repeat the descending and ascending checks for every sortable column.
7. Repeat the same checks for `OOS-LO`, `OOS-NR`, `OOS-CD`, `OOS-NP`, `OOS-LS`, and `OOS-DG`.

## Expected Result

- All seven required ONT status categories are present.
- Each status count matches the corresponding table total.
- Every sortable column is correctly ordered on every page in descending and ascending directions.
- Pagination returns to page 1 after each direction is verified.

## Automation Notes

- The case is marked `@pytest.mark.Unicase`.
- The Map/Device table ID is `Dev_ontStatusTable`.
- A status whose table total is `0` is recorded and skipped because it has no rows whose order can be verified.
- Sorting failures use `with assume`, allowing the remaining columns, directions, and status categories to continue.
- The shared page-sort helper returns the table to page 1 after every direction check.
