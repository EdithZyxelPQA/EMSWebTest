# EMS1-7049 Transceiver Filter

## Purpose

Verify the Inventory / Transceiver filter by device name and main-card slot, then by device IP and NXP test port.

This case does not support the OLT14xx series.

## Marker

`@pytest.mark.Unicase`

## Test data

- Device name and IP are read from `environment_parameter.json`.
- The slot is read from the NXC card for NeoX or the MSC card for IES in `CARDINFO`.
- The port is read from the NXP card in `CARDINFO`.

If the required NXC/MSC or NXP card is absent, the case is skipped with the missing requirement in the reason.

## Steps

1. Open **Inventory / Transceiver**.
2. Open **Filter**.
3. Enter the DUT device name and the NXC/MSC slot, then click **Query**.
4. Read every result page and verify all **Device Name** and **Slot** values.
5. Open **Filter** again and click **Reset**.
6. Enter the DUT IP and the NXP test port, then click **Query**.
7. Read every result page and verify all **IP Address** and **Port** values.

## Expected result

- The first query returns at least one row, and every row has the requested device name and slot.
- The second query returns at least one row, and every row has the requested IP address and port.
