# EMS1-7215 ontServiceEditVlan

## Purpose
Verify that EMS can create an xONT service with 32 QoS service entries and apply VLAN / VLAN Translation values correctly on a NeoX device.

## Scope
- Device: NeoX only
- ONT flag: `xont` only
- EMS URL, DUT, ONT SN, password, and AID are read from `environment_parameter.json`

## Test Steps
1. Login EMS using `EMS.url`, `EMS.login_username`, and `EMS.login_password`.
2. Go to `Provision / Service / ONT / Service`.
3. Filter ONT by the test ONT SN and delete matching service rows.
4. Filter Template by `$py_OntTempVlan` and delete matching service rows.
5. Go to `Provision / Profile`, select `ONT Template Profile`.
6. Delete profile `$py_OntTempVlan` if it exists.
7. Go to `Provision / Profile`, select `ONT Service Profile`.
8. Delete profiles `$py_Service101_XLAN1` through `$py_Service132_XLAN1` if they exist.
9. Recreate profiles `$py_Service101_XLAN1` through `$py_Service132_XLAN1`.
10. For each service profile, set VLAN `101` through `132`, select `XLAN`, and select `LAN 1` in the UNI Port dropdown for XLAN1, then save.
11. Go to `Provision / Profile`, select `ONT QoS Bandwidth Profile`.
12. Delete profiles `$py_Bandwidth_1G_US` and `$py_Bandwidth_1G_DS` if they exist.
13. Recreate profiles `$py_Bandwidth_1G_US` and `$py_Bandwidth_1G_DS`.
14. For each bandwidth profile, set Rate SIR `0`, AIR `0`, PIR `1024000`, and GPON Fallback Rate SIR `0`, AIR `0`, PIR `1024000`, then save.
15. Go to `Provision / Profile`, select `ONT Template Profile`.
16. Create profile `$py_OntTempVlan`.
17. In its Service Table, enable index `1` through `32`.
18. For index `1` through `32`, select service profiles `$py_Service101_XLAN1` through `$py_Service132_XLAN1`.
19. Set each service row US Bandwidth Profile to `$py_Bandwidth_1G_US` and DS Bandwidth Profile to `$py_Bandwidth_1G_DS`.
20. Set Share Priority as `0` through `7`, repeating from `0` at index `9`.
21. In its T-Cont Table, enable index `1` through `8`.
22. For T-Cont index `1`, select Service List `1` through `4`; index `2` selects `5` through `8`; continue through index `8` selecting `29` through `32`.
23. Set each T-Cont row US Bandwidth Profile to `$py_Bandwidth_1G_US`, DS Bandwidth Profile to `$py_Bandwidth_1G_DS`, and Type to `Best-Effort`, then save.
24. Go to `Provision / Service / ONT / Service`.
25. Confirm the Service table has no row for the test ONT SN; delete it if present.
26. Go to `Inventory / ONT`, filter by the test ONT SN.
27. Confirm exactly one matching ONT row exists and its ONT ID is `Unregistered`.
28. Go back to `Provision / Service / ONT / Service`.
29. Click `New Service`.
30. Click `Select ONT`.
31. Enable the SN filter, enter the test ONT SN, click the normal `Search` button, select the matching row, and click `OK`.
32. Open the `{}` editable ONT service row.
33. Enable `Active`.
34. Select ONT Template `$py_OntTempVlan`.
35. In the QoS table, click `New`.
36. Add `service1` through `service32`.
37. For `service1` through `service32`, leave US Bandwidth Profile and DS Bandwidth Profile unchanged.
38. Set VLAN `201` through `232`.
39. Set VLAN Translation SVLAN `301` through `332`.
40. Set VLAN Translation CVLAN `401` through `432`.
41. Save the ONT service.
42. Wait until the service row status becomes `Success`.
43. Go to `Inventory / ONT`, filter by the test ONT SN.
44. Confirm exactly one matching row exists and its ONT ID is not `Unregistered`.
45. SSH to the DUT.
46. Run `show interface remote xont <slot>-<port>-<ont> config`.
47. Verify QoS service index `1` through `32` shows VLAN `201` through `232`, SVLAN `301` through `332`, and CVLAN `401` through `432`.

## Expected Result
- All required service profiles, bandwidth profiles, and the ONT template profile are present.
- EMS creates the ONT service successfully.
- Inventory shows the ONT as registered.
- DUT CLI shows all 32 QoS service VLAN / SVLAN / CVLAN values correctly.
