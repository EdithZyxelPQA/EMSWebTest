# EMS1-7214 deviceStatusDown

## Purpose

Verify EMS updates the DUT to Down after uplink ports are disabled, and verify related Inventory and Dashboard pages show `Device Not Responding`.

## Preconditions

- EMS URL, DUT IP, login account, and password are read from `environment_parameter.json`.
- DUT type must contain `NeoX` or `IES`.
- DUT console must be available. Current test environment uses COM7, 115200, admin/Pqa1234!!.

## Test Steps

1. Login to EMS Web.
2. Enter `Inventory / Device`.
3. Filter the test DUT by IP and confirm `Operational Status` is `Up`.
4. Login to the DUT through console.
5. Run `configure`.
6. Disable uplink ports:
   - NeoX: `interface nni *`, then `disable`.
   - IES: `interface genni *`, then `disable`.
7. Return to EMS `Inventory / Device`.
8. Wait until the DUT `Operational Status` becomes `Down`.
9. Wait about 60 seconds before checking related pages.
10. Enter `Inventory / Card`, filter the DUT, and confirm card `Operation Status` is `Device Not Responding`.
11. Enter `Inventory / Port / All Ports`, filter the DUT, and confirm port `Operation Status` is `Device Not Responding`.
12. Enter `Inventory / Port / Network Port`, filter the DUT, and confirm port `Operation Status` is `Device Not Responding`.
13. Enter `Inventory / Port / Ethernet Access Port`, filter the DUT, and confirm port `Operation Status` is `Device Not Responding` when the DUT has GLC or NXA cards.
14. Enter `Inventory / Port / GPON Port`, filter the DUT, and confirm port `Operation Status` is `Device Not Responding` when the DUT has OLC3416-42A cards or the DUT type contains OLT.
15. Enter `Inventory / Port / xPON Port`, filter the DUT, and confirm port `Operation Status` is `Device Not Responding` when the DUT has OLC3146B, OLC3416B, OLC3816, or NXP cards.
16. Enter `Inventory / ONT`, filter the DUT, and confirm ONT `Operation Status` is `Device Not Responding` when rows exist.
17. Enter `Dashboard / ONT Status`, click each status, select the test DUT when the selector is available, and confirm total data is `0`.
18. Enter `Dashboard / Ethernet Access Port Status`, click `Device Not Responding`, and confirm the DUT appears when the DUT has GLC or NXA cards.
19. Restore the DUT by console:
   - Run `configure`.
   - NeoX: `interface nni *`, then `enable`.
   - IES: `interface genni *`, then `enable`.
20. Return to EMS `Inventory / Device` and wait until the DUT status becomes `Up`.

## Expected Result

`[EMS1-7214][deviceStatusDown] Result passed`

The DUT becomes Down after disabling uplink ports, related inventory/dashboard pages reflect `Device Not Responding`, and the DUT is restored to Up after enabling uplink ports.
