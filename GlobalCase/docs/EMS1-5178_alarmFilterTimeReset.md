# EMS1-5178 Alarm filter Time Reset

## Purpose

Verify that the time-filter Reset button is enabled after entering a time range and restores its initial disabled appearance after clearing the range on both Active and History Alarm pages.

## Marker

`@pytest.mark.Unicase`

## Steps

1. Open **Alarm / Active** and click **Filter**.
2. Enter the current time in **From Time**.
3. Enter the current time plus 10 minutes in **To Time**.
4. Verify that the Reset button changes from its initial gray state to its active green state.
5. Click **Reset**.
6. Verify that From Time and To Time are empty and the Reset button returns to its initial gray state.
7. Repeat steps 1-6 on **Alarm / History**.

## Expected result

- Active and History both enable the Reset button when a time range is entered.
- Reset clears both time fields.
- Reset returns to the `button_gray` inactive class with a gray RGB background.
