# EMS1-6270 ontServiceRegistered

## Scope

- EMS: use `environment_parameter.json`.
- DUT and ONT: use `--cmdopt` and the configured `exe_provision_ont`.
- Page: `Provision / Service / ONT`.

## Test Flow

1. Read the provision test ONT SN, password, and flag from `environment_parameter.json`.
2. Login EMS Web.
3. Enter `Provision / Service / ONT`, filter Serial Number with the test SN, and delete any existing service.
4. SSH to the DUT and unregister the ONT.
   - `xont`: `no interface remote xont sn <sn>` and `no interface remote xont registration-id <pw>`.
   - `ont`: `no interface remote ont sn <sn>` and `no interface remote ont password <pw>`.
   - `ont-14`: `configure`, `no interface remote ont sn <sn>`, and `no interface remote ont password <pw>`.
   - If the CLI asks for delete confirmation, answer `y`.
5. Enter `Inventory / ONT`, filter by the test SN, and repeatedly click Refresh for up to 300 seconds until the ONT ID becomes `Unregistered`. This confirms EMS has synchronized the CLI unregister operation.
6. Filter and compare Inventory rows using the DUT IP, Slot, and Port together. Only for an OLT14 device whose configured Slot is `0`, treat Inventory Slot `0`, `-`, `--`, or blank as the same slot. Other products require an exact non-zero Slot match. Calculate occupied ONT IDs only from this DUT, prefer the configured ONT ID, and use the next available ONT ID only if it is genuinely occupied on the same DUT/Slot/Port.
7. SSH to the DUT and register the ONT.
   - `xont`: `configure`, `interface remote xont <slot>-<port>-<ont>`, `sn <sn>`, `registration-id <pw>`, `no inactive`, `exit`.
   - `ont`: `configure`, `interface remote ont <slot>-<port>-<ont>`, `sn <sn>`, `password <pw>`, `no inactive`, `exit`.
   - `ont-14`: `configure`, `remote ont ont-<port>-<ont>`, `sn <sn>`, `password <pw>`, `no inactive`, `exit`.
8. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with the ONT ID registered by CLI.
9. Enter `Provision / Service / ONT` and click New Service.
10. In the Create ONT Service table, enter the test ONT SN into `Serial Number`.
11. Enter the test ONT password into `Password / Registration ID`.
12. Double-click the `{}` cell to open Edit ONT Service.
13. Enable `Active`, set `Description` to `testRegistered`, and click OK.
14. Back on Create ONT Service, click Save.
15. Wait until the ONT service Status becomes `Success`.
16. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with ONT ID not equal to `Unregistered`.
17. Confirm the Inventory / ONT Description is `testRegistered`.

## Expected Result

`[EMS1-6270][ontServiceRegistered] Result passed`
