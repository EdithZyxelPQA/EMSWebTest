# EMS1-6259 / EMS1-6260 filterOntService

## Scope

- EMS: use `environment_parameter.json`.
- DUT and ONT: use `--cmdopt` and the configured `exe_provision_ont`.
- Page: `Provision / Service / ONT`.

## Test Flow

1. Read the provision test ONT SN, password, and flag from `environment_parameter.json`.
2. SSH to the DUT and unregister the ONT.
   - `xont`: execute `no interface remote xont <slot>-<port>-<ont>` directly at the normal `#` prompt.
   - `ont`: enter `configure`, then execute `no interface remote ont <slot>-<port>-<ont>`.
   - `ont-14`: enter `configure`, then execute `no remote ont ont-<port>-<ont>`.
   - If the CLI asks for delete confirmation, answer `y`.
3. Login EMS Web.
4. Enter `Inventory / ONT`, filter Serial Number with the test SN, and wait until exactly one row exists with ONT ID `Unregistered`.
5. Enter `Provision / Service / ONT`, filter Serial Number with the test SN, and delete any existing service.
6. Enter `Provision / Profile / ONT Template`, recreate an empty profile named `$py_filterTest`.
7. Create a new ONT service:
   - Select the ONT by SN from the Select ONT dialog.
   - Open Edit ONT Service.
   - Enable `Active`.
   - Set `Description` to `testForFilter`.
   - Select ONT Template `$py_filterTest`.
   - Save the service.
8. Wait until the ONT service `Status` becomes `Success`.
9. Click the `Success` link and remember these values, then close the detail dialog:
   - Device Name
   - Device IP
   - Slot
   - Port
   - ONT
   - SN
   - Password
   - Template
   - Status
   - Try the visible `Close` controls in priority order and verify the result modal is invisible. Retry intercepted clicks with JavaScript and use Escape as a final UI fallback; do not continue to Filter while the modal remains visible.
10. For each filter below:
   - Click Filter icon.
   - Click Reset.
   - Enable the target filter checkbox, enter/select the remembered value, and click Query.
   - Verify the filtered table has the expected rows on all pages.
   - If the Service table displays the filtered column, verify every displayed row has the expected value.
   - If the Service table does not display that filtered column, verify the filter returns at least one row because the filter value was taken from the Success detail dialog.
   - Click Filter icon and Reset again.
   - Verify the Service table returns to the unfiltered service result.

## Filter Items

- `SN`: result must contain only one row and SN must equal the test SN.
- `Device Name`: every row Device Name must equal the remembered Device Name.
- `Device IP`: every row Device IP must equal the remembered Device IP.
- `Status`: every row Status must equal the remembered Status.
- `ONT Description`: every row ONT Description must equal `testForFilter`.
- `Slot`: if remembered Slot is not `--` or `0`, every row Slot must equal the remembered Slot.
- `Port`: every row Port must equal the remembered Port.
- `ONT`: every row ONT must equal the remembered ONT.
- `Template`: every row Template must equal `$py_filterTest`.

## Expected Result

`[EMS1-6259][filterOntServiceQuery] Result passed`

`[EMS1-6260][filterOntServiceReset] Result passed`
