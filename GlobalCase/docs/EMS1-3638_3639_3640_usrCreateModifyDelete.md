# EMS1-3638/3639/3640 usrCreateModifyDelete

## Purpose

Verify EMS local-user creation, modification, login/logout, and deletion while local authentication is available.

## Radius Server prerequisite

Before any user operation, open `System / System Properties / System Setting / Radius Server` and verify that `Active` is `Disable`.

- If Active is already Disable, continue without saving.
- If Active is Enable, change it to Disable, click the visible Save or Apply button in the setting page, and require a success result when EMS displays a result dialog.
- Re-read the Active control and require Disable before continuing. Failure to locate, save, or confirm this prerequisite is a hard failure because the local-user login checks would otherwise be invalid.
- Select controls with `Disable` or `Disabled`, checkbox controls, and Disable radio controls are supported.

## Original case flow

After the Radius prerequisite passes, retain the existing case logic:

1. Remove any stale test user/session.
2. Verify invalid create-user inputs and messages.
3. Create the valid local user and verify saved fields.
4. Verify login and logout with the new user.
5. Modify the user and verify modified fields and credentials.
6. Delete the test user and verify cleanup.

## Marks

Keep `@pytest.mark.asyncio` and `@pytest.mark.Unicase`.
