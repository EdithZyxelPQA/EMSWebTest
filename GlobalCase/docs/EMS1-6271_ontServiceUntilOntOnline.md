# EMS1-6271 ontServiceUntilOntOnline

## Scope

- EMS: use `environment_parameter.json`.
- DUT and ONT: use `--cmdopt` and the configured `exe_provision_ont`.
- Page: `Provision / Service / ONT`.

## Test Flow

1. Read the provision test ONT SN, password, flag, slot, and port from `environment_parameter.json`.
2. SSH to the DUT and unregister the ONT.
   - `xont`: `no interface remote xont sn <sn>` and `no interface remote xont registration-id <pw>`.
   - `ont`: `no interface remote ont sn <sn>` and `no interface remote ont password <pw>`.
   - `ont-14`: `configure`, `no interface remote ont sn <sn>`, and `no interface remote ont password <pw>`.
   - If the CLI asks for delete confirmation, answer `y`.
3. SSH to the DUT and disable the PON port connected to the ONT.
   - `xont`: `configure`, `interface xpon <slot>-<port>`, `inactive`, `exit`, `exit`.
   - `ont`: `configure`, `interface gpon <slot>-<port>`, `inactive`, `exit`, `exit`.
   - `ont-14`: `configure`, `interface olt pon-<port>`, `inactive`, `exit`, `exit`.
4. Login EMS Web.
5. Enter `Inventory / ONT`, filter Serial Number with both 16-digit and 12-digit SN, and wait until the ONT does not exist.
6. Enter `Provision / Service / ONT`, filter Serial Number with the test SN, and delete any existing service.
7. Click New Service.
8. In the Create ONT Service table, enter the test ONT SN into `Serial Number`.
9. Enter the test ONT password into `Password / Registration ID`.
10. Double-click the `{}` cell to open Edit ONT Service.
11. Enable `Active` and click OK.
12. Back on Create ONT Service, click Save.
13. Confirm the ONT service Status stays `Wait` for at least 1 minute.
14. SSH to the DUT and enable the PON port connected to the ONT.
   - `xont`: `configure`, `interface xpon <slot>-<port>`, `no inactive`, `exit`, `exit`.
   - `ont`: `configure`, `interface gpon <slot>-<port>`, `no inactive`, `exit`, `exit`.
   - `ont-14`: `configure`, `interface olt pon-<port>`, `no inactive`, `exit`, `exit`.
15. Wait until the ONT service Status becomes `Success`.
16. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with ONT ID not equal to `Unregistered`.

## Cleanup

If the test fails after disabling the PON port, the automation enables the PON port again in `finally`.

## Expected Result

`[EMS1-6271][ontServiceUntilOntOnline] Result passed`
