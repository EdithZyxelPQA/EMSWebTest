# EMS1-6269 ontServiceUnregistered

## Scope

- EMS: use `environment_parameter.json`.
- DUT and ONT: use `--cmdopt` and the configured `exe_provision_ont`.
- Page: `Provision / Service / ONT`.

## Test Flow

1. Read the provision test ONT SN, password, and flag from `environment_parameter.json`.
2. SSH to the DUT and unregister the ONT.
   - `xont`: execute `no interface remote xont <slot>-<port>-<ont>` directly at the normal `#` prompt; do not enter `configure` mode first.
   - `ont`: enter `configure`, then execute `no interface remote ont <slot>-<port>-<ont>`.
   - `ont-14`: enter `configure`, then execute `no remote ont ont-<port>-<ont>`.
   - If the CLI asks for delete confirmation, answer `y`.
3. Login EMS Web.
4. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with ONT ID `Unregistered`.
5. Enter `Provision / Service / ONT`, filter Serial Number with the test SN, and delete any existing service.
6. Click New Service.
7. In the Create ONT Service table, enter the test ONT SN into `Serial Number`.
8. Enter the test ONT password into `Password / Registration ID`.
9. Double-click the `{}` cell to open Edit ONT Service.
10. Enable `Active` and click OK.
11. Back on Create ONT Service, click Save.
12. Wait until the ONT service Status becomes `Success`.
13. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with ONT ID not equal to `Unregistered`.

## Expected Result

`[EMS1-6269][ontServiceUnregistered] Result passed`

## Diagnostic Output

- After sending the unregister command, print the exact command and complete CLI response.
- Print `ONT unregister CLI error detected: YES` when the response contains an existing CLI error keyword; otherwise print `NO`.
- This output does not change the command, test sequence, pass/fail conditions, or timeout behavior.
