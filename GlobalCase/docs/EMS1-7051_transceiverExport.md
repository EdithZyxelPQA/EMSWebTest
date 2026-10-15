# EMS1-7051 Transceiver Export

## Purpose

Verify that Inventory / Transceiver exports a non-empty file whose contents match the table shown on the EMS web page.

## Marker

`@pytest.mark.Unicase`

## Steps

1. Open **Inventory / Transceiver**.
2. Capture the currently displayed Transceiver table contents.
3. Click the **Export** icon.
4. Wait up to 60 seconds for a newly downloaded `.xls` file.
5. Verify the downloaded file size is greater than zero.
6. Compare the exported rows and comparable columns with the captured web table.

## Expected result

- A new `.xls` file is downloaded within 60 seconds.
- The exported file size is greater than zero.
- The exported data matches the Transceiver table displayed when Export was clicked.
