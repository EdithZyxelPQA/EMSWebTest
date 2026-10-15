# EMS1-7072 Transceiver Information

## Purpose

Verify that Inventory / Transceiver information filtered by the DUT IP matches the `portinfo` Transceiver data in the device RESTful dev JSON uploaded to EMS.

## Marker

`@pytest.mark.Unicase`

## Supported devices

OLT14xx-series devices are not supported. When the DUT type contains `OLT14`, the case is reported as skipped without collecting RESTful debug files or opening the Transceiver page.

## RESTful debug collection

1. Record the original device and performance upload UUID/path MIB values.
2. Temporarily set the UUID values to `<device IP>_dev` and `<device IP>_perf`.
3. Temporarily set the upload paths to the DevicePollerDebug and PerformanceDebug paths on the configured EMS server.
4. Download both JSON files from `/opt/ELEMENTVIEW_MASTER/bin` on the EMS server.
5. Restore all four original MIB values in a `finally` block, including when collection fails.

The downloaded artifacts are saved under `report/` with the `EMS1-7072_` prefix.

## Steps

1. Open **Inventory / Transceiver**.
2. Open **Filter**, reset existing conditions, enter the DUT IP, and click **Query**.
3. Read all result pages.
   Each row and all its comparison columns are captured atomically from the same DOM `<tr>` so a live refresh cannot combine a Slot from one row with a Port from another row.
4. Build the expected Transceiver rows from RESTful `portinfo` entries where any Vendor Name, Vendor PN, Vendor Revision, Vendor SN, Vendor DC, Transceiver type, or Calibration field is non-empty. A row is not excluded merely because Vendor PN is blank.
5. Match EMS and RESTful entries by Slot ID and Port ID.
6. Compare Device Name, IP Address, Slot, Port, Vendor Name, Vendor PN, Vendor Revision, Vendor SN, Vendor DC, Transceiver type, and Calibration.

Empty strings, `--`, and `null` are treated as equivalent because EMS renders empty RESTful values with placeholders.

The Unicode replacement character `�` is removed before comparison. Some legacy transceiver values contain invalid source bytes: EMS renders those bytes as `�`, while the RESTful JSON reader drops them. Only `�` is removed; other characters and Slot/Port entries must still match.

## Expected result

- OLT14xx-series devices report SKIP.
- EMS and RESTful JSON contain the same Transceiver Slot/Port entries.
- Every compared Transceiver field is consistent.
- The original RESTful upload MIB values are restored after collection.
